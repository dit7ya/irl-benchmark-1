''' Module containing reward functions to be used for IRL '''

from collections import namedtuple
from copy import copy

from gym.envs.toy_text.discrete import DiscreteEnv
from gym.spaces.discrete import Discrete as DiscreteSpace
from gym.wrappers.time_limit import TimeLimit

import numpy as np

State = namedtuple('State', ('state'))
StateAction = namedtuple('StateAction', ('state', 'action'))
StateActionState = namedtuple('StateActionState', ('state', 'action', 'next_state'))


class AbstractRewardFunction(object):
    ''' The (abstract) superclass for reward functions
    '''

    def __init__(self, env, \
                 action_in_domain=False, next_state_in_domain=False):
        '''
        env: a gym environment
        action_in_domain: domain of reward function contains actions - R(s, a) or R(s, a, s')
        next_state_in_domain: domain of reward function contains next state - R(s, a, s')
        '''
        self.env = env
        self.action_in_domain = action_in_domain
        if next_state_in_domain:
            assert action_in_domain
        self.next_state_in_domain = next_state_in_domain

    def domain(self):
        ''' Return the domain of the reward function as a namedtuple, either State, StateAction, or StateActionState.
        This might not be implemented for big environments, they use domain_sample instead. '''
        raise NotImplementedError()

    def domain_sample(self, batch_size):
        ''' Sample a batch from the domain of the reward function. 
        batch_size: how many inputs to sample.
        Returns a namedtuple, either State, StateAction, or StateActionState
        '''
        raise NotImplementedError()

    def reward(self, domain_batch):
        ''' Return corresponding rewards for a domain batch (see domain() / domain_sample())
        '''
        raise NotImplementedError()

    def update_parameters(self, parameters):
        ''' Update the parameters of the reward function '''
        self.parameters = parameters


class TabularRewardFunction(AbstractRewardFunction):
    ''' A tabular reward function where rewards for each possible input are stored in a table.
    Only suitable for relatively small environments '''
    
    def __init__(self, env, parameters=None,\
                 action_in_domain=False, next_state_in_domain=False):
        super(TabularRewardFunction, self).__init__(env, action_in_domain, next_state_in_domain)
        
        # this reward function is only implemented for discrete state and action space
        assert isinstance(env.observation_space, DiscreteSpace)
        assert isinstance(env.action_space, DiscreteSpace)
        # calculate number of elements in domain:
        self.domain_size = self.env.observation_space.n
        if self.action_in_domain:
            self.domain_size *= self.env.action_space.n
        if self.next_state_in_domain:
            self.domain_size *= self.env.observation_space.n

        # if environment is certain discrete gym environment, 
        # we can automatically extract reward table:
        if parameters is 'extract_automatically' and isinstance(env, TimeLimit) \
                    and issubclass(type(env.env), DiscreteEnv):
            assert self.action_in_domain and not self.next_state_in_domain
            parameters = []
            domain = self.domain()
            for index in range(self.domain_size):
                outcomes = self.env.env.P[domain.state[index]][domain.action[index]]
                parameters.append(np.sum([outcomes[j][0] * outcomes[j][2] for j in range(len(outcomes))]))

        assert len(parameters) == self.domain_size
        self.parameters = np.array(parameters)

    def domain(self):
        ''' Return the domain of the reward function. Returns a namedtuple, either State, StateAction, or StateActionState '''
        # domain always contains states:
        states = np.arange(self.env.observation_space.n)
        if self.action_in_domain:
            # if domain contains actions: extend domain
            states = np.repeat(states, self.env.action_space.n)
            actions = np.arange(self.env.action_space.n)
            actions = np.tile(actions, self.env.observation_space.n)
            if self.next_state_in_domain:
                # if domain contains next states: extend domain
                states = np.repeat(states, self.env.observation_space.n)
                actions = np.repeat(actions, self.env.observation_space.n)
                next_states = np.arange(self.env.observation_space.n)
                next_states = np.tile(next_states, self.env.observation_space.n * self.env.action_space.n)
                # return the adequate namedtuple:
                return StateActionState(states, actions, next_states)
            return StateAction(states, actions)
        return State(states)

    def domain_sample(self, batch_size):
        ''' Returns a sample of the domain of size batch_size '''
        raise NotImplementedError()

    def domain_to_index(self, domain_batch):
        ''' Convert a domain batch into corresponding indices of the reward table '''
        index = copy(domain_batch.state)
        if self.action_in_domain:
            index *= self.env.action_space.n
            index += domain_batch.action
            if self.next_state_in_domain:
                index *= self.env.observation_space.n
                index += domain_batch.next_state
        return index

    def reward(self, domain_batch):
        ''' Return the corresponding rewards of a domain_batch. '''
        indices = self.domain_to_index(domain_batch)
        return self.parameters[indices]


class FeatureBasedRewardFunction(AbstractRewardFunction):

    def __init__(self, env, parameters):
        super(FeatureBasedRewardFunction, self).__init__(env, parameters)
        self.parameters = parameters

    def reward(self, domain_batch):
        ''' Return corresponding rewards for a domain batch (see domain() / domain_sample())
        '''
        reward = np.dot(self.parameters, domain_batch)
        return reward

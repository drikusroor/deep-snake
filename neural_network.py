import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, Sequential, optimizers
from constants import *
from enums.direction import *
import matplotlib.pyplot as plt

from envs.deep_snake_env import DeepSnakeEnv


class NeuralNetwork:

    def __init__(self, env: DeepSnakeEnv, path=None) -> None:

        self.env = env  # import env

        self.state_shape = env.observation_space.shape  # the state space
        self.action_shape = env.action_space.n  # the action space
        self.gamma = 0.9  # decay rate of past observations
        self.alpha = 1e-4  # learning rate in the policy gradient
        self.learning_rate = 0.01  # learning rate in deep learning

        if not path:
            self.model = self._create_model()  # build model
        else:
            self.model = tf.keras.models.load_model(path)  # import model

        # record observations
        self.states = []
        self.gradients = []
        self.rewards = []
        self.probs = []
        self.discounted_rewards = []
        self.total_rewards = []

    def _create_model(self):
        ''' builds the model using keras'''
        model = Sequential()

        # input shape is of observations
        # model.add(layers.CategoryEncoding(num_tokens=4)),
        model.add(layers.Dense(observation_shape,
                  input_shape=(observation_shape,), activation="relu"))
        # add a relu layer
        model.add(layers.Dense(observation_shape * 2, activation="relu"))

        # output shape is according to the number of action
        # The softmax function outputs a probability distribution over the actions
        model.add(layers.Dense(3, activation="softmax"))
        model.compile(loss="categorical_crossentropy",
                      optimizer=optimizers.Adam(lr=self.learning_rate))

        model.build((None, ROWS_AMOUNT * COLS_AMOUNT))

        print(model.summary())

        return model

    def hot_encode_action(self, action):
        '''encoding the actions into a binary list'''

        action_encoded = np.zeros(self.action_shape, np.float32)
        action_encoded[action] = 1

        return action_encoded

    def remember(self, state, action, action_prob, reward):
        '''stores observations'''
        encoded_action = self.hot_encode_action(action)
        self.gradients.append(encoded_action-action_prob)
        self.states.append(state)
        self.rewards.append(reward)
        self.probs.append(action_prob)

    def get_action(self, state):
        '''samples the next action based on the policy probabilty distribution 
        of the actions'''

        # transform state
        state = state.reshape(1, -1)
        # get action probably
        action_probability_distribution = self.model.predict(
            state, batch_size=1).flatten()
        # norm action probability distribution

        # sample action
        action = np.random.choice(a=self.action_shape, size=1,
                                  p=action_probability_distribution)

        return action, action_probability_distribution

    def get_discounted_rewards(self, rewards):
        '''Use gamma to calculate the total reward discounting for rewards
        Following - \gamma ^ t * Gt'''

        discounted_rewards = []
        cumulative_total_return = 0
        # iterate the rewards backwards and and calc the total return
        for reward in rewards[::-1]:
            cumulative_total_return = (
                cumulative_total_return*self.gamma)+reward
            discounted_rewards.insert(0, cumulative_total_return)

        # normalize discounted rewards
        mean_rewards = np.mean(discounted_rewards)
        std_rewards = np.std(discounted_rewards)
        norm_discounted_rewards = (discounted_rewards -
                                   mean_rewards)/(std_rewards+1e-7)  # avoiding zero div

        return norm_discounted_rewards

    def update_policy(self):
        '''Updates the policy network using the NN model.
        This function is used after the MC sampling is done - following
        \delta \theta = \alpha * gradient + log pi'''

        # get X
        states = np.array(self.states).reshape(-1, observation_shape)

        # get Y
        gradients = np.vstack(self.gradients)
        rewards = np.vstack(self.rewards)
        discounted_rewards = self.get_discounted_rewards(rewards)
        gradients *= discounted_rewards
        gradients = self.alpha*np.vstack([gradients])+self.probs

        X = states
        y = gradients

        history = self.model.train_on_batch(X, y)

        self.states, self.probs, self.gradients, self.rewards = [], [], [], []

        return history

    def train(self, episodes, rollout_n=1, render_n=50):
        '''train the model
            episodes - number of training iterations 
            rollout_n- number of episodes between policy update
            render_n - number of episodes between env rendering '''

        env = self.env
        total_rewards = np.zeros(episodes)
        total_steps = np.zeros(episodes)

        for episode in range(episodes):
            # each episode is a new game env
            env.reset()
            state = env.game.get_observation()
            done = False
            episode_reward = 0  # record episode reward
            steps = 0

            while not done:
                # play an action and record the game state & reward per episode
                steps += 1
                action, prob = self.get_action(state)
                next_state, reward, done, _ = env.step(action)
                self.remember(state, action, prob, reward)
                state = next_state
                episode_reward += reward

                # if episode%render_n==0: ## render env to visualize.
                if RENDER_MODE == 'human':
                    env.render()
                if done:
                    # update policy
                    if episode % rollout_n == 0:
                        print('Episode: %d, Reward: %d, Steps: %d' %
                              (episode, episode_reward, steps))
                        history = self.update_policy()

            total_rewards[episode] = episode_reward
            total_steps[episode] = steps

        self.episodes = np.array(range(episodes)) + 1
        self.total_rewards = total_rewards
        self.total_steps = total_steps

    def plot(self):
        '''Plots the reward per episode'''
        plt.plot(self.episodes, self.total_rewards)
        plt.plot(self.episodes, self.total_steps, '-.')
        plt.xlabel('Episodes')
        plt.ylabel('Total Reward (-)')
        plt.show()

    def save_model(self, path):
        '''Saves the model to the specified path'''
        self.model.save(path)

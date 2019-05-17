import config
from classifier.train import train

if __name__ == '__main__':
    train(config.train_data_path, config.naive_bayes_model_path)

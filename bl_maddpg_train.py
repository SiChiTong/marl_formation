from baselines import logger

from multirobot.ddpg.environment import DdpgEnv
from multirobot.environment import make_env
from multirobot.util import parse_args

try:
    from mpi4py import MPI
except ImportError:
    MPI = None


def configure_logger(log_path, **kwargs):
    if log_path is not None:
        logger.configure(log_path)
    else:
        logger.configure(**kwargs)


def train(arglist):
    # Create environment
    env = make_env(arglist.scenario, arglist, arglist.benchmark)
    ddpg_env = DdpgEnv(env)
    from multirobot.maddpg.maddpg import learn

    if MPI is None or MPI.COMM_WORLD.Get_rank() == 0:
        rank = 0
        configure_logger(arglist.log_path)
    else:
        rank = MPI.COMM_WORLD.Get_rank()
        configure_logger(arglist.log_path, format_strs=[])

    learn(network="mlp",
          env=ddpg_env,
          # total_timesteps=400,
          nb_epoch_cycles=3,
          nb_rollout_steps=400,
          nb_epochs=3000,
          render=arglist.display,
          normalize_observations=False,
          normalize_returns=False)


if __name__ == '__main__':
    arglist = parse_args()
    train(arglist)

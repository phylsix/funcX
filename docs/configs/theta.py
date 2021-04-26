from funcx_endpoint.endpoint.utils.config import Config
from funcx_endpoint.executors import HighThroughputExecutor
from parsl.providers import CobaltProvider
from parsl.launchers import AprunLauncher
from parsl.addresses import address_by_hostname

# PLEASE UPDATE user_opts BEFORE USE
user_opts = {
    'theta': {
        'worker_init': 'source ~/setup_funcx_test_env.sh',
        'scheduler_options': '',
        # Specify the account/allocation to which jobs should be charged
        'account': '<YOUR_THETA_ALLOCATION>'
    }
}

config = Config(
    executors=[
        HighThroughputExecutor(
            max_workers_per_node=1,
            address=address_by_hostname(),
            provider=CobaltProvider(
                queue='debug-flat-quad',
                account=user_opts['theta']['account'],
                launcher=AprunLauncher(overrides="-d 64"),
                # string to prepend to #COBALT blocks in the submit
                # script to the scheduler eg: '#COBALT -t 50'
                scheduler_options=user_opts['theta']['scheduler_options'],

                # Command to be run before starting a worker, such as:
                # 'module load Anaconda; source activate funcx_env'.
                worker_init=user_opts['theta']['worker_init'],

                walltime='00:30:00',
                nodes_per_block=2,
                init_blocks=1,
                min_blocks=1,
                max_blocks=1,
            ),
        )
    ],
)

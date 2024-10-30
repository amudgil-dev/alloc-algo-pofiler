from app.models.hetro_jobs import (
    JobClass,
)

from app.utils.statistics import SimStats


class RunParamA:

    VARY_N = [10, 100, 500, 1000, 1500, 2000, 2500, 3000]
    VARY_BETA = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    @staticmethod
    def get_vary_n():
        return RunParamA.VARY_N

    @staticmethod
    def get_vary_beta():
        return RunParamA.VARY_BETA

    @staticmethod
    def get_params(n):
        myparams = {"n": n, "beta": 0.3, "alpha": 0, "d_n": 10}
        return myparams

    @staticmethod
    def get_job_classes():
        job_classes = {
            "A": JobClass(
                "A",
                # arrival_rate=0.3,
                arrival_rate=0,
                mean_size=1,
                parallelism=5,
                speedup_function=lambda x: x**0.8,
                generate_job_size_function=lambda: SimStats.generate_exponential_job_size(
                    1
                ),
                pstar_alloc_strategy={"type": "fixed", "servers": 3},
            ),
            "B": JobClass(
                "B",
                # arrival_rate=0.5,
                arrival_rate=0,
                mean_size=4,
                parallelism=8,
                speedup_function=lambda x: x**0.7,
                generate_job_size_function=lambda: SimStats.generate_exponential_job_size(
                    4
                ),
                pstar_alloc_strategy={"type": "fixed", "servers": 3},
            ),
            "C": JobClass(
                "C",
                # arrival_rate=0.3,
                arrival_rate=0,
                mean_size=5,
                parallelism=10,
                speedup_function=lambda x: x**0.9,
                generate_job_size_function=lambda: SimStats.generate_exponential_job_size(
                    5
                ),
                pstar_alloc_strategy={"type": "fixed", "servers": 3},
            ),
            "D": JobClass(
                "D",
                arrival_rate=0.1,
                mean_size=0.7,
                parallelism=13,
                # speedup_function=lambda x: x**0.6,
                speedup_function=lambda x: x**0.1,
                generate_job_size_function=lambda: SimStats.generate_exponential_job_size(
                    0.7
                ),
                pstar_alloc_strategy={"type": "fixed", "servers": 3},
            ),
            "E": JobClass(
                "E",
                arrival_rate=0.2,
                # arrival_rate=0.0,
                mean_size=1.2,
                parallelism=10,
                speedup_function=lambda x: x**0.5,
                generate_job_size_function=lambda: SimStats.generate_exponential_job_size(
                    1.2
                ),
                pstar_alloc_strategy={"type": "fixed", "servers": 3},
            ),
        }

        return job_classes

    # Data for each distribution
    @staticmethod
    def get_distribution():
        distributions = {
            "Deterministic": {
                "wait_n": {
                    10: 0.05481110421498182,
                    100: 0.0010931358572806968,
                    500: 1.6592340991721244e-06,
                    1000: 0.0,
                    1500: 0.0,
                    2000: 0.0,
                    2500: 0.0,
                    3000: 0.0,
                },
                "processing_n": {
                    10: 0.6357711694385106,
                    100: 0.3710818978076796,
                    500: 0.3470240297306257,
                    1000: 0.3434624636973715,
                    1500: 0.3434003981718896,
                    2000: 0.3433307431217254,
                    2500: 0.3434122206183658,
                    3000: 0.343022939671145,
                },
            },
            "Exponential": {
                "wait_n": {
                    10: 0.43498751558501125,
                    100: 0.00483400639307758,
                    500: 0.00025600093897380744,
                    1000: 1.470099244987523e-05,
                    1500: 1.3224249735970753e-06,
                    2000: 5.06967219482135e-07,
                    2500: 0.0,
                    3000: 0.0,
                },
                "processing_n": {
                    10: 0.9924116713157918,
                    100: 0.4498411080806196,
                    500: 0.3614568026142152,
                    1000: 0.35120701517532493,
                    1500: 0.3462482554350492,
                    2000: 0.3462178951367314,
                    2500: 0.3430550437306205,
                    3000: 0.34838848073651196,
                },
            },
            "Mixed-Erlang": {
                "wait_n": {
                    10: 0.061723856981590865,
                    100: 0.001400141703070242,
                    500: 1.3821163322575102e-07,
                    1000: 0.0,
                    1500: 0.0,
                    2000: 0.0,
                    2500: 0.0,
                    3000: 0.0,
                },
                "processing_n": {
                    10: 0.6306416413360685,
                    100: 0.37740244692251285,
                    500: 0.3469220041012635,
                    1000: 0.34356876238702455,
                    1500: 0.3429796781217878,
                    2000: 0.3439157646005375,
                    2500: 0.34325282209582936,
                    3000: 0.34368182035455,
                },
            },
            "Perato": {
                "wait_n": {
                    10: 0.17140335173973234,
                    100: 0.0009335808321681014,
                    500: 1.0946181098026387e-06,
                    1000: 0.0,
                    1500: 0.0,
                    2000: 0.0,
                    2500: 0.0,
                    3000: 0.0,
                },
                "processing_n": {
                    10: 0.8378559584430385,
                    100: 0.3387773554448771,
                    500: 0.3484068273313858,
                    1000: 0.3406545595507049,
                    1500: 0.34421092477374426,
                    2000: 0.3300635913771784,
                    2500: 0.4646586195952789,
                    3000: 0.3348790174753533,
                },
            },
        }
        return distributions

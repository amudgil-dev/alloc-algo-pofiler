import matplotlib.pyplot as plt

from simdata.sim_parameters import RunParamA

distributions = RunParamA.get_distribution()

# # Data from the provided results
# distributions = {
#     "Deterministic": {
#         "wait_n": {
#             10: 0.05481110421498182,
#             100: 0.0010931358572806968,
#             500: 1.6592340991721244e-06,
#             1000: 0.0,
#             1500: 0.0,
#             2000: 0.0,
#             2500: 0.0,
#             3000: 0.0,
#         },
#         "processing_n": {
#             10: 0.6357711694385106,
#             100: 0.3710818978076796,
#             500: 0.3470240297306257,
#             1000: 0.3434624636973715,
#             1500: 0.3434003981718896,
#             2000: 0.3433307431217254,
#             2500: 0.3434122206183658,
#             3000: 0.343022939671145,
#         },
#     },
#     "Exponential": {
#         "wait_n": {
#             10: 0.43498751558501125,
#             100: 0.00483400639307758,
#             500: 0.00025600093897380744,
#             1000: 1.470099244987523e-05,
#             1500: 1.3224249735970753e-06,
#             2000: 5.06967219482135e-07,
#             2500: 0.0,
#             3000: 0.0,
#         },
#         "processing_n": {
#             10: 0.9924116713157918,
#             100: 0.4498411080806196,
#             500: 0.3614568026142152,
#             1000: 0.35120701517532493,
#             1500: 0.3462482554350492,
#             2000: 0.3462178951367314,
#             2500: 0.3430550437306205,
#             3000: 0.34838848073651196,
#         },
#     },
#     "Mixed-Erlang": {
#         "wait_n": {
#             10: 0.061723856981590865,
#             100: 0.001400141703070242,
#             500: 1.3821163322575102e-07,
#             1000: 0.0,
#             1500: 0.0,
#             2000: 0.0,
#             2500: 0.0,
#             3000: 0.0,
#         },
#         "processing_n": {
#             10: 0.6306416413360685,
#             100: 0.37740244692251285,
#             500: 0.3469220041012635,
#             1000: 0.34356876238702455,
#             1500: 0.3429796781217878,
#             2000: 0.3439157646005375,
#             2500: 0.34325282209582936,
#             3000: 0.34368182035455,
#         },
#     },
#     "perato": {
#         "wait_n": {
#             10: 0.19228106973691264,
#             100: 0.0012430178220940449,
#             500: 0.0,
#             1000: 0.0,
#             1500: 0.0,
#             2000: 0.0,
#             2500: 0.0,
#             3000: 0.0,
#         },
#         "processing_n": {
#             10: 0.6953751726981012,
#             100: 0.34279533361984044,
#             500: 0.3484790205738718,
#             1000: 0.33806102573774066,
#             1500: 0.3350712286478656,
#             2000: 0.348194971375448,
#             2500: 0.33840925347954276,
#             3000: 0.3370242333498444,
#         },
#     },
# }

# Prepare data
n_values = [10, 100, 500, 1000, 1500, 2000, 2500, 3000]
distributions_list = list(distributions.keys())

# Colors and line styles for the plots
colors = ["b", "g", "r", "c"]
markers = ["s", "^", "o", "*"]
line_styles = ["-", "--", "-.", ":"]

# Plot wait_n against n
plt.figure(figsize=(10, 5))
for i, dist in enumerate(distributions_list):
    wait_n_values = [distributions[dist]["wait_n"].get(n, 0) for n in n_values]
    plt.plot(
        n_values,
        wait_n_values,
        color=colors[i],
        linestyle=line_styles[i],
        label=f"{dist} (wait_n)",
        linewidth=2,
    )

plt.title("Wait Time (wait_n) vs n", fontsize=14)
plt.xlabel("n", fontsize=12, weight="bold")
plt.ylabel("wait_n", fontsize=12, weight="bold")
plt.legend()
plt.grid(True)
plt.tick_params(axis="both", which="major", labelsize=10, width=2)
plt.tick_params(axis="both", which="minor", width=1)
plt.show()

# Plot processing_n against n
plt.figure(figsize=(10, 5))
for i, dist in enumerate(distributions_list):
    processing_n_values = [
        distributions[dist]["processing_n"].get(n, 0) for n in n_values
    ]
    plt.plot(
        n_values,
        processing_n_values,
        color=colors[i],
        linestyle=line_styles[i],
        label=f"{dist} (processing_n)",
        linewidth=2,
    )

plt.title("Processing Time (processing_n) vs n", fontsize=14)
plt.xlabel("n", fontsize=12, weight="bold")
plt.ylabel("processing_n", fontsize=12, weight="bold")
plt.legend()
plt.grid(True)
plt.tick_params(axis="both", which="major", labelsize=10, width=2)
plt.tick_params(axis="both", which="minor", width=1)
plt.show()

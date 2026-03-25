import matplotlib.pyplot as plt
import arviz as az


def get_channel_contributions(mmm):
    return mmm.compute_channel_contribution()


def plot_channel_contributions(contrib):
    mean_contrib = contrib.mean(dim=["chain", "draw"])

    fig, ax = plt.subplots()
    mean_contrib.to_pandas().plot(kind="bar", ax=ax)

    ax.set_title("Channel Contribution")
    ax.set_ylabel("Contribution")

    return fig


def plot_response_curves(mmm):
    return mmm.plot_response_curves()


def plot_posterior_diagnostics(idata):
    return az.plot_trace(idata)


def compute_marginal_roas(mmm):
    return mmm.compute_channel_contribution().mean(dim=["chain", "draw"])
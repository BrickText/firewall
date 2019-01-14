import matplotlib.pyplot as plt

__all__ = [
    "plot_decisions",
]


def plot_decisions(model, X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Test Set
    X_plot = PCA(n_components=1).fit_transform(X_test)
    plt.scatter(X_plot, y_test)
    plt.plot(X_plot, y_pred, c='r')

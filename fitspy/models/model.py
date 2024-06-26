class Model:
    def __init__(self):
        pass

    def newDocument(self):
        print("New document is requested")

    def toggle_plot_fit(self, state):
        if state == 2:  # Qt.Checked
            print("Plot Fit is checked")
        else:
            print("Plot Fit is unchecked")
        
    def toggle_plot_neg_values(self, state):
        if state == 2:
            print("Plot Neg Values is checked")
        else:
            print("Plot Neg Values is unchecked")

    def toggle_plot_outliers(self, state):
        if state == 2:
            print("Plot Outliers is checked")
        else:
            print("Plot Outliers is unchecked")

    def toggle_plot_outliers_limits(self, state):
        if state == 2:
            print("Plot Outliers Limits is checked")
        else:
            print("Plot Outliers Limits is unchecked")

    def toggle_plot_noise_level(self, state):
        if state == 2:
            print("Plot Noise Level is checked")
        else:
            print("Plot Noise Level is unchecked")

    def toggle_plot_baseline(self, state):
        if state == 2:
            print("Plot Baseline is checked")
        else:
            print("Plot Baseline is unchecked")

    def toggle_plot_background(self, state):
        if state == 2:
            print("Plot Background is checked")
        else:
            print("Plot Background is unchecked")

    def toggle_plot_residuals(self, state):
        if state == 2:
            print("Plot Residuals is checked")
        else:
            print("Plot Residuals is unchecked")
    
    def toggle_show_peaks_labels(self, state):
        if state == 2:
            print("Show Peaks Labels is checked")
        else:
            print("Show Peaks Labels is unchecked")

    def update_residual_coeff(self, text):
        print("Residual coefficient is changed to", text)
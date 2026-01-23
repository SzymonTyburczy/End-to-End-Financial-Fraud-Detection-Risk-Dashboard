import shap
import matplotlib.pyplot as plt

class ModelEvaluator:
    def __init__(self, model):
        self.model = model

    def explain_with_shap(self, X):
        """Generating features chart."""
        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values(X)
        
        shap.summary_plot(shap_values, X, show=False)
        plt.savefig("models/shap_summary.png")
        print("📊 Chart SHAP saved in models/shap_summary.png")
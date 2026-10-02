"""Real evaluation — actual sklearn metrics computed on a held-out split.
Never reports a single accuracy number in isolation; always includes
per-class precision/recall/F1 so class imbalance can't hide behind a
flattering top-line accuracy."""
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix


def evaluate_model(model, X_test, y_test, class_names: list[str]) -> dict:
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision, recall, f1, support = precision_recall_fscore_support(
        y_test, y_pred, labels=class_names, average=None, zero_division=0
    )
    macro_f1 = f1.mean() if len(f1) else 0.0
    cm = confusion_matrix(y_test, y_pred, labels=class_names).tolist()

    per_class = {
        cls: {"precision": round(float(p), 3), "recall": round(float(r), 3),
              "f1": round(float(f), 3), "support": int(s)}
        for cls, p, r, f, s in zip(class_names, precision, recall, f1, support)
    }

    return {
        "accuracy": round(float(accuracy), 3),
        "macro_f1": round(float(macro_f1), 3),
        "per_class": per_class,
        "confusion_matrix": cm,
        "test_set_size": len(y_test),
    }

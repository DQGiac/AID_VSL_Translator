import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.model_selection import StratifiedKFold
import joblib

parameters_dict = {
    "boosting_type": "gbdt",
    "objective": "multiclass",
    "metric": "multi_logloss",
    "num_class": 1,
    "verbosity": -1,
    'n_estimators': 315, 
    'learning_rate': 0.038927375208580535, 
    'max_depth': 4, 
    'min_data_in_leaf': 274, 
    'subsample_freq': 9, 
    'feature_fraction': 0.36072715109677717, 
    'reg_lambda': 79.31416605346095, 
    'reg_alpha': 3.2965928880922615, 
    'subsample': 0.9862207095636681,
}

csv = pd.read_csv("csv_2_hands.csv")
csv.index = [i for i in range(len(csv))]
classes = csv.drop(["target"], axis=1)
target = csv["target"]

skf = StratifiedKFold(shuffle=True, random_state=12)
a = (skf.split(classes, target))
for train_index, test_index in skf.split(classes, target):
    X_train, X_valid = classes.iloc[train_index], classes.iloc[test_index]
    y_train, y_valid = target.iloc[train_index], target.iloc[test_index]

# print(X_train[5:30])

model = LGBMClassifier(**parameters_dict)
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, "2_hand_model.pkl")

# n = 0
y_val_p = model.predict_proba(X_valid)
# y_val_p_arr = [[i for i in j] for j in y_val_p]
# maximum = 0
# minimum = float("inf")
# for i in y_valid.index:
#     maximum = max(maximum, (max(y_val_p_arr[i])))
#     minimum = min(minimum, (max(y_val_p_arr[i])))
#     print(maximum, minimum)
    # if y_valid[i] != cols[y_val_p_arr[i].index(max(y_val_p_arr[i]))]:
    #     n += 1
# print(1 - n / len(y_valid))
# lgb.save_model("lgbm.h5")
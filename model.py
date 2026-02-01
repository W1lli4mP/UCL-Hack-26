import catboost as cb
from catboost import CatBoostRegressor, Pool
from sklearn.model_selection import train_test_split, GridSearchCV
import matplotlib as plt

from sklearn.pipeline import Pipeline
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score

df = pd.read_parquet("./data/training_data.parquet")
df["year"] = df["dateoftransfer".str[:4]].astype(int)
df = df.drop(columns=["dateoftransfer"])

X = df.drop(columns=["price"])
y = df["price"]

categorical_features = [
    'postcode',
    'propertytype',
    'CURRENT_ENERGY_RATING',
    "FLOOR_TYPE",
    "FLOOR_INSULATED",
    "WINDOWS_TYPE",
    "WINDOWS_DEGREE",
    "WALLS_TYPE",
    "WALLS_CAVITY",
    "WALLS_INSULATED",
    "ROOF_TYPE",
    "ROOF_INSULATED",
    "MAINHEAT_TYPE",
    'MAINHEAT_ENERGY_EFF'
]


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

train_pool = Pool(data=X_train, label=y_train, cat_features=categorical_features)

test_pool = Pool(data=X_test, label=y_test, cat_features=categorical_features)

params = dict(
    task_type="GPU",
    devices="0",
    loss_function="MAE",
    depth=6,
    learning_rate=0.05,
    iterations=1000,
    subsample=0.8,
    random_seed=42,
    od_type="Iter",
    od_wait=150,
    thread_count=-1
)

# attempt to use GPU to speed up process; falling back to CPU when failing
try:
    model = CatBoostRegressor(task_type="GPU", devices="0", **params)
    model.fit(train_pool, eval_set=test_pool, use_best_model=True)
except Exception:
    model = CatBoostRegressor(task_type="CPU", **params)
    model.fit(train_pool, eval_set=test_pool, use_best_model=True)


preds = model.predict(test_pool)

mae = mean_absolute_error(y_test, preds)
r2 = r2_score(y_test, preds)
print("MAE:", mae)
print("R²:", r2)

importances = model.get_feature_importance(train_pool)
feature_names = X_train.columns

for name, score in sorted(zip(feature_names, importances), key=lambda x: -x[1]):
    print(f"{name}: {score:.2f}")
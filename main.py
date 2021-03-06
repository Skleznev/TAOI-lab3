import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.tree import export_graphviz
from six import StringIO
from IPython.display import Image
import pydotplus

col_names = ['PUPIL_SEX','PUPIL_CLASS','TEACHER_RIGHT','TEACHER_CHK','TEACHER_QUEST','TEACHER_CORR','PUPIL_CORR','PUPIL_STRIP','GRADE']
tree = pd.read_csv(r"grades.csv", header = None, names = col_names)
tree.head()

feature_cols = ['PUPIL_SEX','PUPIL_CLASS','TEACHER_RIGHT','TEACHER_CHK','TEACHER_QUEST','TEACHER_CORR','PUPIL_CORR','PUPIL_STRIP']
X = tree[feature_cols] # Features
y = tree.GRADE # Target variable

for criterion in ['gini', 'entropy']:
    for size in [0.4, 0.3, 0.2, 0.1]:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = size, random_state = 1)

        clf = DecisionTreeClassifier(criterion)
        clf = clf.fit(X_train,y_train)

        y_pred = clf.predict(X_test)

        result = confusion_matrix(y_test, y_pred)
        print("Confusion Matrix:")
        print(result)
        result1 = classification_report(y_test, y_pred)
        print("Classification Report:",)
        print (result1)
        result2 = accuracy_score(y_test,y_pred)
        print("Accuracy:",result2)

        dot_data = StringIO()
        export_graphviz(clf, out_file=dot_data, filled=True, rounded=True,
           special_characters=True,feature_names = feature_cols,class_names=['2','3','3-','4','4-','5','5-'])

        graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
        graph.write_png('graphs/'+ criterion +'/Tree_' + str(size) + '.png')
        Image(graph.create_png())

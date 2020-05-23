from recommender import algo
from load_data import data,item_list
import random


# building model on training data
trainingSet = data.build_full_trainset()
algo.fit(trainingSet)


def generate_weights(user_id,item_list,algo):
    """generates a list of items based on their weights"""   
    # generates predictions
    def rating_pred(user_id,item_list,algo):
        pred = {}
        for i in item_list:
            prediction = algo.predict(user_id, i)
            pred[i] = prediction.est
        return pred
    
    # generates weights 
    weighted_list = []
    pred = rating_pred(user_id,item_list,algo)
    
    for i in pred.keys():
        if pred[i] <0: # if the predicted rating is negative
            weighted_list += [i]
        elif pred[i] <0.9: # if the predicted rating < 0.9
            weighted_list += 2 * [i]
        else: # if pred == 1
            weighted_list += 3 * [i]
    return weighted_list


def generate_recommendation(user_id,item_list,algo):
    weighted_l = generate_weights(user_id,item_list,algo)
    return random.choice(weighted_l)

if __name__ == "__main__":
    app.run(debug=False)

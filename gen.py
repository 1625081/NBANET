import pickle
import numpy as np
import random
import copy
import gc
filename = "train.p"
given_length = 5
predict_period = 2
total_len = given_length + predict_period
#test_list= pickle.load(open(filename , "rb" ))
#print("Load Success!\n")
#recover = copy.deepcopy(test_list)
#print("Copy Success!\n")

for count in range(200):
    output = [] # data used for train/test
    gt_data = [] # ground truth data
    output_filename = "tests/test_data_"+str(count)+".p"
    gt_data_filename = "answers/gt_data_"+str(count)+".p"
    test_list= pickle.load(open(filename , "rb" ))
    print("Load Success!")
    #test_list = copy.deepcopy(recover)
    #print("Copy Success!\n")    
    for event in test_list:
        if len(event.moments) > 200:
    
            duration = int(event.moments[0].game_clock - event.moments[-1].game_clock)
    
            game_clock_list = []
            game_clock_s_list = []
            for moment in event.moments:
                if int(moment.game_clock) not in game_clock_s_list:
                    game_clock_s_list.append(int(moment.game_clock))            
                    game_clock_list.append(moment.game_clock)
            data_list = game_clock_list[2:-2] # remove first and last 2 seconds
            if len(data_list) > 10:
                random_index = random.randrange(0,len(data_list[:-7]))
                index_list = range(random_index, random_index+total_len, 1)
                choosen_time = np.asarray(game_clock_list)[index_list]
                choosen_time = np.delete(choosen_time, 5) # remove 6th second data
                given_seq = choosen_time[:5]
                predict_seq = choosen_time[-1]
            
                test_data = []
                pred_data = []
                for moment in event.moments:
                    # print moment.game_clock, predict_seq,moment.game_clock == predict_seq
                    if moment.game_clock in list(given_seq):
                        test_data.append(moment)
                    elif moment.game_clock == predict_seq:
                        pred_data = moment
                rand_player = random.choice(pred_data.players) # select a random player from list
                ground_truth = (rand_player.x, rand_player.y)
                rand_player.x = -1
                rand_player.y = -1
                test_data.append(pred_data)
                # ground_truth
                gt_data.append(ground_truth)
                output.append(test_data)
    
    pickle.dump(output, open(output_filename , "wb" ))
    pickle.dump(gt_data, open(gt_data_filename , "wb" ))
    print("Circle "+str(count)+" is done.")
    del test_list
    gc.collect()

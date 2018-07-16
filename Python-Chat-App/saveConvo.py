import pandas as pd
import basic_crf
from preProcess import preProcess
import os

utterance_number = 0
current_speaker = ""
first_speaker = True
previous_speaker = ""
count = 0


def remove_file(filename):
    cwd = os.getcwd()
    directory = str(cwd)
    to_delete = directory + "\\" + filename
    os.remove(to_delete)


def find_utterance_number(speaker):
    global utterance_number, current_speaker, previous_speaker, first_speaker
    current_speaker = speaker
    if first_speaker:
        first_speaker = False
        utterance_number = 1
        previous_speaker = current_speaker
    elif previous_speaker == current_speaker:
        utterance_number += 1
    elif previous_speaker != current_speaker:
        utterance_number = 1
        previous_speaker = current_speaker

    return utterance_number


def get_utterance_thread(speaker):
    global utterance_number, current_speaker, first_speaker, previous_speaker
    utterance_number = 0
    current_speaker = ""
    first_speaker = True
    previous_speaker = ""
    thread_number = find_utterance_number(speaker)
    return thread_number


def save_conversation(conversation):
    global count
    temp_df = pd.DataFrame(columns=['speaker', 'thread_number', 'label', 'type', 'pos', 'utterance'])
    predicted_data = pd.DataFrame(columns=['speaker', 'utterance'])
    for utterance in conversation:
        sentence = str(utterance['message'])
        speaker = str(utterance['user_name'])

        predicted_data.loc[-1] = [speaker, sentence]
        predicted_data.index = predicted_data.index + 1

        # Convert to lower case
        sentence = sentence.lower()

        # Replace http... with url
        sentence = preProcess.replace_http_url(sentence)

        # Replace www.... with email
        sentence = preProcess.replace_email(sentence)

        # Replace numbers with string numbers
        sentence = preProcess.replace_numbers(sentence)

        # Replace @u_name with username
        sentence = preProcess.replace_username(sentence)

        # Replace emoticon with pos or neg emotion
        sentence = preProcess.replace_emoticon(sentence)

        # Remove stop words from the utterance
        sentence = preProcess.remove_stop_words(sentence)

        # Extract the pos of each token
        pos_tag = preProcess.get_pos(sentence)

        # Get the conversation thread number
        num_utterance = find_utterance_number(speaker)

        temp_df.loc[-1] = [speaker, num_utterance, "", "", pos_tag, sentence]
        temp_df.index = temp_df.index + 1

    # update file count
    count = count + 1

    # Save to test folder
    filename = "testData/" + str(count) + ".csv"
    temp_df.to_csv(filename, index=False)

    # Running the predictive model
    training_dir_path = "trainData"
    test_dir_path = "testData\\"
    y_prediction = basic_crf.test_accuracy(training_dir_path, test_dir_path)
    predicted_data['label'] = y_prediction[0]

    # Remove the file from test folder
    remove_file(filename)

    # Save to results folder
    filename = "results/" + str(count) + ".csv"
    predicted_data.to_csv(filename, index=False)






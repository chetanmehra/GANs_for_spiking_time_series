import sys

from evaluator import Evaluator

sys.path.append("..")
import os

timesteps = 90
elements = 10
split = 0.3
targets = 20
iterations_number = 5

transactions_filepath = '../../datasets/berka_dataset/usable/normalized_transactions_months.npy'
models_list = ['nn', 'svm']

base_folder = 'models_comparison'
if not os.path.exists(base_folder):
    os.mkdir(base_folder)

for iteration in range(iterations_number):
    flattening_ranges = [0.0, 0.05, 0.1, 0.15, 0.2]

    for flattening_range in flattening_ranges:
        evaluator = Evaluator(models_list, transactions_filepath, split, elements, timesteps, targets, flattening_range,
                              iteration)

        labels = ['vae', 'wgan_gp', 'wgan_gp_packing', 'wgan_gp_vae']
        if flattening_range == 0.0:
            labels.append('handcrafted')

        title = 'models_comparison'

        base_filepath = 'comparison_datasets/'
        end_filename = 'generated_datasets/1000000_generated_data.npy'
        generated_data_filepaths = []
        for label in labels:
            generated_data_filepaths.append(base_filepath + label + '/' + end_filename)

        evaluator.set_base_folder(base_folder)
        evaluator.run_comparison_classification(generated_data_filepaths, labels, title)
        print(flush=True)

    #-------------------------------------------------------
    flattening_range = 0.15
    evaluator = Evaluator(models_list, transactions_filepath, split, elements, timesteps, targets, flattening_range,
                          iteration)

    model = 'wgan_gp_packing'

    title = 'training_comparison'

    base_filepath = 'comparison_datasets/' + model + '/generated_datasets/'
    end_filename = '_generated_data.npy'

    generated_data_filepaths = []
    labels = [str(i) for i in range(100000, 1000001, 100000)]
    for label in labels:
        generated_data_filepaths.append(base_filepath + label + end_filename)

    evaluator.set_base_folder(base_folder)
    evaluator.run_comparison_classification(generated_data_filepaths, labels, title)
    print(flush=True)

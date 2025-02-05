from dataset import load_jsonl_file

file_path1 = '../../data/comment_results/inference/init/inference_results_final.jsonl'
file_path2 = '../../data/comment_results/inference/cur/inference_results_final-v2.jsonl'

data1 = load_jsonl_file(file_path1)
data2 = load_jsonl_file(file_path2)

n = 10

for i in range(n):
    assert data1[i]['original_comment'] == data2[i]['original_comment']
    print('='*50, i, '='*50)
    print(data1[i]['prompt'].split('### Code changes:')[1].split('### Response:')[0])
    print('+='*50)
    print('\n')
    print('\033[1;32m INIT - Original comment: \033[1;37m', data1[i]['original_comment'])
    print('\033[1;35m INIT - Generated comment \033[1;37m', data1[i]['genrated_comment'])
    print('+='*50)
    print('\033[1;34m CUR - Reformulated comment  \033[1;37m', data2[i]['reformulated_comment'])
    print('\033[1;35m CUR - Generated comment \033[1;37m', data2[i]['genrated_comment'])
    print('\n')



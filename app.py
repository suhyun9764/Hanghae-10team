from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/memo/")
def memo():

    # 예시 메모
    memo_list = []
    for i in range(100):
        memo = {
            'text': i+1,
            'date': i+2000
        }
        memo_list.append(memo)

    memo_per_page= 6
    # 클라이언트의 현재 페이지 숫자(없으면 기본적으로 1페이지)
    page = request.args.get('page',1,type=int)

    # 내보내야 할 데이터 정보의 start index와 end index
    start_index = (page-1)*memo_per_page
    end_index = start_index+memo_per_page

    # 내보낼 메모들 리스트로 저장
    current_page_memo = memo_list[start_index:end_index]

    total_memos = len(memo_list)
    total_pages = (total_memos+memo_per_page-1)//memo_per_page
    
    return render_template('memo.html', data=current_page_memo, page_num=total_pages)


if __name__ == '__main__':
    app.run()

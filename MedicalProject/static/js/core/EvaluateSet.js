class EvaluateSet {
    constructor(attempt_id, set_id, get_evaluation_question_url, csrf_token, evaluate_url) {
        this.csrf_token = csrf_token;
        this.submit_response_url = evaluate_url;
        this.get_evaluation_question_url = get_evaluation_question_url;
        this.attempt_id = attempt_id;
        this.set_id = set_id;
    }

    start(load_dicom) {
        this.load_dicom = load_dicom;
        this.fetch_questions();
        if (this.num_questions > 0) {
            this.display_question(0);
            console.log("test has been started with the first question");
            this.current_question_counter = 0;
        } else {
            console.log("It has no questions");
        }


    }

    fetch_questions() {
        console.log('tring to fetch questions from ' + this.get_evaluation_question_url);
        let questions = [];
        $.ajax({
            'url': this.get_evaluation_question_url,
            'type': 'post',
            async: false,
            data: {
                'attempt_pk': this.attempt_id,
                'csrfmiddlewaretoken': this.csrf_token,
            },
            dataType: 'json',
            success: function (data) {
                questions = data['question_set'];
                console.log(questions.length);

                console.log("question fetched successfully");
                return questions;


            }
        });

        this.num_questions = questions.length;
        console.log(questions);
        let question;
        this.question_set = [];
        for (let i = 0; i < this.num_questions; i++) {
            let res = questions[i].res;
            let correct_ans = questions[i].correct_ans;
            let ans_text = questions[i].ans_text;
            console.log(questions[i]);
            question = new EvaluateQuestion(questions[i].question_id, questions[i].image_url, this.set_id, res, correct_ans, ans_text);
            // question = "";
            this.question_set.push(question);
        }

    }

    display_question(question_counter) {
        if (question_counter >= 0 && question_counter < this.num_questions) {
            let question = this.question_set[question_counter];
            console.log(this.question_set[question_counter].image_url);
            load_dicom(this.question_set[question_counter].image_url);
            console.log(question);
            console.log("current question counter:" + question_counter);
            this.current_question_counter = question_counter;
            $("#ques_number").html(parseInt(question_counter) + 1);
            question.fill_response_box();


            this.update_navigations();
        } else {
            alert("invalid");
        }

    }

    previous_question() {
        if (parseInt(this.current_question_counter) > 0) {
            this.display_question(this.current_question_counter - 1);
        } else {
            console.log("You can't go back");
        }

    }

    next_question() {
        if (parseInt(this.current_question_counter) < (this.num_questions - 1)) {
            this.display_question(this.current_question_counter + 1);
        } else {
            console.log("You can't go next");
        }
    }


    update_navigations() {
        $("#navigation-box").empty();
        for (let i = 0; i < this.num_questions; i++) {
            let question_number = i + 1;
            let btn = "" +
                "<button value='" + i + "' class=\"btn btn-outline-info rounded-circle m-1 p-0\" style=\"width: 40px;height: 40px\"><span>" + question_number + "</span></button>\n";
            if (i === parseInt(this.current_question_counter)) {
                btn = "" +
                    "<button value='" + i + "' class=\"btn btn-info rounded- m-1 p-0\" style=\"width: 40px;height: 40px\"><span>" + question_number + "</span></button>\n";
            }
            $("#navigation-box").append(btn);
        }
    }


    mark_correct_for(counter) {
        this.question_set[counter].mark_as_correct(this.submit_response_url, this.csrf_token);

    }


    set_finish() {
        console.log('test evaluation has been finished');
        setTimeout(function () {
            location.href = "/modules/attempted-sets";
        }, 500)
    }

}

class EvaluateQuestion {
    constructor(question_id, image_url, set_id, res, correct_ans, ans_text) {
        this.image_url = image_url;
        this.question_id = question_id;
        this.set_id = set_id;
        this.ans_text = ans_text;
        this.res = res;
        this.correct_ans = correct_ans;
    }

    fill_response_box() {
        if (this.correct_ans === 1) {
            $("#correct_normal_btn").removeClass('btn-outline-success').addClass('btn-success');
            $("#correct_abnormal_btn").removeClass('btn-success').addClass('btn-outline-success');
            $("#correct_ans_box").hide();
            console.log('corresct ans is normal')

        } else {
            $("#correct_abnormal_btn").removeClass('btn-outline-success').addClass('btn-success');
            $("#correct_normal_btn").removeClass('btn-success').addClass('btn-outline-success');
            $("#correct_ans_box").show().val(this.ans_text);
            console.log("correst ans is abnormal " + this.ans_text);
        }

        if (this.res) {
            $("#res_box").show();
            if (this.res.ans_type === 1) {
                $("#res_normal_btn").removeClass('btn-outline-info').addClass('btn-info');
                $("#res_abnormal_btn").removeClass('btn-info').addClass('btn-outline-info');
                $("#res_ans_box").hide();

            } else {
                $("#res_abnormal_btn").removeClass('btn-outline-info').addClass('btn-info');
                $("#res_normal_btn").removeClass('btn-info').addClass('btn-outline-info');
                $("#res_ans_box").show().val(this.res.ans_text);


            }

        } else {
            $("#res_box").hide();
            $("#res_ans_box").hide();
        }

    }


    mark_as_correct(evaluate_response_url, csrf_token) {
        $.ajax({
            'url': evaluate_response_url,
            'type': 'post',
            data: {
                'set_pk': this.set_id,
                'res_pk': this.res.pk,
                'is_correct': true,
                'csrfmiddlewaretoken': csrf_token,
            },
            dataType: 'json',
            success: function (data) {
                console.log('res marked as correct');
            }
        })
    }

}
class AttemptSet {
    constructor(set_id, user_id, get_question_url, csrf_token, submit_response_url) {
        this.csrf_token = csrf_token;
        this.submit_response_url = submit_response_url;
        this.get_question_url = get_question_url;
        this.set_id = set_id;
        this.user_id = user_id;

    }

    start(load_dicom) {
        this.seconds = 0;
        this.load_dicom = load_dicom;
        this.fetch_questions();
        if (this.num_questions > 0) {
            this.display_question(0);
            console.log("test has been started with the first question");
            this.current_question_counter = 0;
            // timer should be start now
        } else {
            console.log("It has no questions");
        }

    }

    fetch_questions() {
        console.log('tring to fetch questions from ' + this.get_question_url);
        let questions = [];
        $.ajax({
            'url': this.get_question_url,
            'type': 'post',
            async: false,
            data: {
                'set_pk': this.set_id,
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
            question = new Question(questions[i].question_id, questions[i].image_url, this.set_id);
            // question = "";
            this.question_set.push(question);
        }

    }

    display_question(question_counter) {
        question_counter = parseInt(question_counter);
        if (question_counter >= 0 && question_counter < this.num_questions) {
            let question = this.question_set[question_counter];
            console.log(this.question_set[question_counter].image_url);
            load_dicom(this.question_set[question_counter].image_url);
            console.log(question);
            console.log("current question counter:" + question_counter);
            this.current_question_counter = question_counter;
            $("#ques_number").html(parseInt(question_counter) + 1);
            $("#res_ans_box").hide();
            this.update_navigations();
        } else {
            alert("invalid");
        }

    }

    previous_question() {
        if (parseInt(this.current_question_counter) > 0) {
            let qc = this.current_question_counter;
            this.display_question(this.current_question_counter - 1);
        this.question_set[qc].submit_response(this.submit_response_url, this.csrf_token);
        } else {
            console.log("You can't go back");
        }

    }

    next_question() {
        if (parseInt(this.current_question_counter) < (this.num_questions - 1)) {
            let qc = this.current_question_counter;
            this.display_question(this.current_question_counter + 1);
        this.question_set[qc].submit_response(this.submit_response_url, this.csrf_token);
        } else {
            console.log("You can't go next");
        }
    }



    // set_timer() {
    //     this.seconds++;
    //     // console.log(Number.isNaN(this.seconds));
    //     $("#timer").html(this.seconds + " MIN")
    //
    // }

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

    set_response_for_ques(normal, abnormal, text){
        let q = this.question_set[this.current_question_counter];
        q.set_response(normal, abnormal, text);
    }

    submit_response_for(counter){
        this.question_set[counter].submit_response(this.submit_response_url, this.csrf_token);
    }


    set_finish() {
        clearInterval(this.tid);
        this.question_set[this.current_question_counter].submit_response(this.submit_response_url, this.csrf_token);
        // call to ajax and mark test as finished
        // send it to answer page
        console.log('test has been finished');
        $("#test-box").html("Test has been finished. <span class='text-danger'> after 5 seconds you will be redirected to attempted sets page</span>");
        setTimeout(function () {
            location.href = "/modules/attempted-sets";
        }, 5000)
    }


}


class Question {

    constructor(question_id, image_url, set_id) {
        this.image_url = image_url;
        this.question_id = question_id;
        this.set_id = set_id;
        this.response = {
            'normal': false,
            'abnormal': false,
        };
    }

    set_response(normal, abnormal, text) {
        if (normal) {
            this.response.normal = true;
            this.response.abnormal = false;
        } else {
            this.response.normal = false;
            this.response.abnormal = {
                'text': text,
            };
        }
        console.log('set response done..');
        console.log(this.response);
    }

    submit_response(submit_response_url, csrf_token) {
        console.log('trying to submit the rsesponse');
        console.log(this.response);
        let data = {};

        if (this.response.normal) {
            data = {
                'csrfmiddlewaretoken': csrf_token,
                'set_pk': this.set_id,
                'question_pk': this.question_id,
                'normal': true,
            }
        } else if(this.response.abnormal){
            data = {
                'csrfmiddlewaretoken': csrf_token,
                'set_pk': this.set_id,
                'question_pk': this.question_id,
                'abnormal': true,
                'answer_text':this.response.abnormal.text,
            }
        }
        console.log(data);
        $.ajax({
            url: submit_response_url,
            type: 'post',
            async:true,
            data: data,
            dataType: 'json',
            success:function (res_data) {
                console.log("response saved");
                $("#num_answered").html(res_data['num_answered']);
                $("#num_unanswered").html(res_data['num_unanswered']);
            }
        })
        //here we will submit the response via ajax
    }


}
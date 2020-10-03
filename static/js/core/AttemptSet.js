class AttemptSet {
    constructor(set_id, user_id){
        this.set_id = set_id;
        this.user_id = user_id;

    }

    start(load_dicom){
        this.load_dicom = load_dicom;
        this.fetch_questions();
        if(this.num_questions>0){
            this.display_question(0);
            console.log("test has been started with the first question");
            this.current_question_counter = 0;
            // timer should be start now
        } else {
            console.log("It has no questions");
        }

    }
    fetch_questions(get_question_url, csrf_token){

        let questions = [
            {
                'question_id':1,
                'image_url':'images/0002.DCM',
            },
            {
                'question_id':2,
                'image_url':'images/0002.DCM',
            },
            {
                'question_id':3,
                'image_url':'images/0002.DCM',
            },
            {
                'question_id':4,
                'image_url':'images/0002.DCM',
            },
            {
                'question_id':5,
                'image_url':'images/0002.DCM',
            },
        ];
        this.num_questions = questions.length;
        let question;
        this.question_set = [];
        for(let i=0;i<this.num_questions;i++){
            question = new Question(questions[i].question_id,questions[i].image_url, this.set_id);
            // question = "";
            this.question_set.push(question);
        }
    }

    display_question(question_counter){
        if(question_counter>=0 && question_counter<this.num_questions){
            let question = this.question_set[question_counter];
            console.log(this.question_set[question_counter].image_url);
            load_dicom(this.question_set[question_counter].image_url);
            console.log(question);
            console.log("current question counter:" + question_counter);
            this.current_question_counter = question_counter;
            $("#ques_number").html(parseInt(question_counter)+1);
            $("#res_ans_box").hide();
            this.update_navigations();
        }
        else {
            alert("invalid");
        }

    }
    previous_question(){
        if(parseInt(this.current_question_counter)>0){
            this.display_question(this.current_question_counter-1)

        } else {
            console.log("You can't go back");
        }

    }
    next_question(){
        if(parseInt(this.current_question_counter)<(this.num_questions-1)){
            this.display_question(this.current_question_counter+1)
        } else {
            console.log("You can't go next");
        }
    }
    set_timer(){
        // tid = setInterval()
    }

    // on select or on submit
    submit_response_for(question, response) {
        question.submit_response(this.user_id, response, this.CSRF_TOKEN, this.SUBMIT_RESPONSE_URL);
        console.log("trying to submit the response for " + question.question_id);
        if(res==='success'){
            this.answered_questions++;
            this.unanswered_questions = this.num_questions-this.unanswered_questions;
            console.log('response has been submitted for question ', question);
        }
    }

    update_navigations(){
        $("#navigation-box").empty();
        for(let i=0;i<this.num_questions;i++){
            let question_number = i+1;
            let btn = "" +
                "<button value='"+i+"' class=\"btn btn-outline-info rounded-circle m-1 p-0\" style=\"width: 40px;height: 40px\"><span>"+question_number+"</span></button>\n";
            if(i === parseInt(this.current_question_counter)){
                btn = "" +
                    "<button value='"+i+"' class=\"btn btn-info rounded- m-1 p-0\" style=\"width: 40px;height: 40px\"><span>"+question_number+"</span></button>\n";
            }
            $("#navigation-box").append(btn);
        }
    }



    set_finish(){
        // call to ajax and mark test as finished
        // send it to answer page
        console.log('test has been finished');
        $("#test-box").html("Test has been finished.");
    }


}





class Question{

    constructor(question_id,image_url, set_id) {
        this.image_url = image_url;
        this.question_id = question_id;
        this.set_id=set_id;
    }

    submit_response(user_id, response){
        this.question_id;
        return {'res':'success'}
        //here we will submit the response via ajax
    }



}
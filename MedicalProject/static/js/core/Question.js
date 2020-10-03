class Question{

    response = {
      'normal':'normal',
      'abnormal':{
          'answer':'',
      },
    };

    constructor(question_id, set_id) {
        this.image_url = "";
        this.question_id = question_id;
        this.set_id=set_id;
    }

    submit_response(user_id, response, csrf_token, submit_response_url){
        this.question_id;
        return {'res':'success'}
        //here we will submit the response via ajax
    }



}

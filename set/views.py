from django.shortcuts import render, redirect, get_object_or_404
from .models import Module, Set, Question, Response, AttemptedSet
from django.http import JsonResponse


def list_modules(request):
    if request.user.is_authenticated:
        modules = Module.objects.all()
        context = {
            'modules': modules
        }
        return render(request, 'modules.html', context)
    return redirect('/')


def module_sets_list(request, module_pk):
    if request.user.is_authenticated:
        module = get_object_or_404(Module, pk=module_pk)
        sets = module.set_set.all()
        # todo separate attempted sets and non-attempted sets
        context = {
             'module': module,
            'sets': sets,
        }
        return render(request, 'sets.html', context)
    return redirect('/')


def attemp_set(request, set_pk):
    if request.user.is_authenticated:
        set = get_object_or_404(Set, pk=set_pk)
        try:
            attemp = AttemptedSet.objects.get(set=set, user=request.user)
        except AttemptedSet.DoesNotExist:
            attemp = None
        if attemp is None:
            context = {
                'set': set,
            }
            return render(request, 'attempt.html', context)
        return redirect("/modules/modules/" + str(set.module.pk))
    return redirect('/')


def attempted_sets(request):
    if request.user.is_authenticated:
        attempted = AttemptedSet.objects.filter(user=request.user)
        context = {
            'attempted': attempted,
        }
        return render(request, 'attempted-sets.html', context)
    return redirect('/')


def evaluate(request, set_pk):
    if request.user.is_authenticated:
        set = get_object_or_404(Set, pk=set_pk)
        try:
            attempt = AttemptedSet.objects.get(set=set, user=request.user)
        except AttemptedSet.DoesNotExist:
            attempt = None
        if attempt is not None:
            context = {
                'attempt': attempt
            }
            return render(request, 'evaluate.html', context)
        else:
            return redirect('/set/attempted-sets')
    return redirect('/')


def result(request, set_pk):
    if request.user.is_authenticated:
        set = get_object_or_404(Set, pk=set_pk)
        try:
            attempt = AttemptedSet.objects.get(set=set, user=request.user)
        except AttemptedSet.DoesNotExist:
            attempt = None
        if attempt is not None:
            if attempt.is_evaluated:

                num_answered = attempt.num_answered
                num_correct = attempt.num_correct
                num_questions = attempt.num_questions

                import math

                percentage = math.floor((num_correct / num_questions) * 100)

                context = {
                    'attempt': attempt,
                    'num_questions': num_questions,
                    'num_answered': num_answered,
                    'num_correct': num_correct,
                    'percentage': percentage,
                }

                return render(request, 'result.html', context)
            else:
                attempted = AttemptedSet.objects.filter(user=request.user)
                context = {
                    'attempted': attempted,
                    'err': "Evaluate first",
                }
                return render(request, 'attempted-sets.html', context)
        else:
            return redirect('/modules/attempted-sets')
    return redirect('/')
def admin_result(request, set_pk):
    if request.user.is_superuser:
        set = get_object_or_404(Set, pk=set_pk)
        try:
            attempt = AttemptedSet.objects.get(set=set, user=request.user)
        except AttemptedSet.DoesNotExist:
            attempt = None
        if attempt is not None:
            if attempt.is_evaluated:

                num_answered = attempt.num_answered
                num_correct = attempt.num_correct
                num_questions = attempt.num_questions

                import math

                percentage = math.floor((num_correct / num_questions) * 100)

                context = {
                    'attempt': attempt,
                    'num_questions': num_questions,
                    'num_answered': num_answered,
                    'num_correct': num_correct,
                    'percentage': percentage,
                }

                return render(request, 'resultforadmin.html', context)
        else:
            return redirect('/modules/admin-panel/attempted-sets')
    return redirect('/admin-panel/')


# JQUERY
def get_questions(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            set_pk = request.POST.get('set_pk', None)
            print(set_pk)
            try:
                set = Set.objects.get(pk=set_pk)
            except Set.DoesNotExist:
                set = None
            if set is not None:
                questions = set.question_set.all()
                question_set = []
                for q in questions:
                    file_url = str(q.get_file_url())
                    question_set.append({
                        'question_id': q.pk,
                        'image_url': file_url,
                    })
                    print(question_set)
                return JsonResponse({'question_set': question_set})
            return JsonResponse({'question_set': []})


def submit_response(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            set_pk = request.POST.get('set_pk', None)
            question_pk = request.POST.get('question_pk', None)
            normal = request.POST.get('normal', False)
            abnormal = request.POST.get('abnormal', False)
            answer_text = request.POST.get('answer_text', None)
            try:
                set = Set.objects.get(pk=set_pk)
            except Set.DoesNotExist:
                set = None
            if set is not None:
                try:
                    attempt = AttemptedSet.objects.get(set=set, user=request.user)
                except AttemptedSet.DoesNotExist:
                    attempt = AttemptedSet(set=set, user=request.user)
                    attempt.save()

                try:
                    question = Question.objects.get(pk=question_pk)
                except Question.DoesNotExist:
                    question = None
                if question is not None:
                    try:
                        response = Response.objects.get(attempt=attempt, question=question)
                    except Response.DoesNotExist:
                        response = Response(attempt=attempt, question=question)

                    if normal:
                        response.ans_type = 1
                        response.save()
                    elif abnormal:
                        response.ans_type = 2
                        response.ans_text = answer_text
                        response.save()
                num_answered = attempt.response_set.count()
                num_unanswered = set.question_set.count() - attempt.response_set.count()
                return JsonResponse({'msg': 'success', 'num_answered': num_answered, 'num_unanswered': num_unanswered})


def get_questions_along_with_responses_for_evaluation(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            attempt_pk = request.POST.get('attempt_pk', None)
            try:
                attempt = AttemptedSet.objects.get(pk=attempt_pk, user=request.user)
            except AttemptedSet.DoesNotExist:
                attempt = None
            if attempt is not None:
                questions = attempt.set.question_set.all()
                print(questions.count())
                question_set = []
                for q in questions:
                    file_url = str(q.get_file_url())
                    res = q.response_set.filter(attempt=attempt, question=q).first()
                    if res:
                        res = {
                            'ans_type': res.ans_type,
                            'ans_text': res.ans_text,
                            'is_correct': res.is_correct,
                            'pk': res.pk,
                        }
                    else:
                        res = None
                    question_set.append({
                        'pk': q.pk,
                        'image_url': file_url,
                        'res': res,
                        'correct_ans': q.ans_type,
                        'ans_text': q.ans_text,
                    })
                return JsonResponse({'question_set': question_set})
            return JsonResponse({'question_set': []})


def evaluate_response(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            set_pk = request.POST.get('set_pk', None)
            res_pk = request.POST.get('res_pk', None)
            is_correct = request.POST.get('is_correct', None)
            try:
                set = Set.objects.get(pk=set_pk)
            except Set.DoesNotExist:
                set = None
            print(set_pk, res_pk, is_correct)
            if set is not None:
                try:
                    attempt = AttemptedSet.objects.get(set=set, user=request.user)
                except AttemptedSet.DoesNotExist:
                    attempt = None
                if attempt is not None:
                    attempt.is_evaluated = True
                    attempt.num_answered = attempt.response_set.count()
                    attempt.num_correct = attempt.response_set.filter(is_correct=True).count()
                    attempt.num_questions = set.question_set.count()
                    attempt.save()
                    try:
                        res = Response.objects.get(pk=res_pk)
                    except Response.DoesNotExist:
                        res = None
                    if res is not None and is_correct:
                        if is_correct:
                            res.is_correct = True
                            res.save()
                            attempt.num_correct = attempt.response_set.filter(is_correct=True).count()
                            attempt.save()

                    return JsonResponse({'msg': 'success'})


# FOR ADMIN

def admin_modules(request):
    if request.user.is_superuser:
        modules = Module.objects.all()
        return render(request, 'admin-modules.html', {'modules':modules})
    return redirect('/admin-panel/')


def admin_add_module(request):
    if request.user.is_superuser:
        if request.method == "POST":
            name = request.POST.get('name', None)
            description = request.POST.get('description', None)

            module = Module(name=name, description=description)
            module.save()
            return redirect('/modules/admin-panel/modules/')
        else:
            return render(request, 'admin-add-module.html')
    return redirect('/admin-panel/')

def delete_module(request):
    if request.user.is_superuser:
        if request.is_ajax():
            module_pk = request.POST.get('module_pk', None)
            if module_pk:
                module = get_object_or_404(Module, pk=module_pk)
                module.delete()
                return JsonResponse({'msg':'success'})

def admin_sets(request, module_pk):
    if request.user.is_superuser:
        module = get_object_or_404(Module, pk=module_pk)
        sets = module.set_set.all()
        return render(request, 'admin-sets.html', {'sets':sets, 'module':module})


def view_set(request, set_pk):
    if request.user.is_superuser:
        set = get_object_or_404(Set, pk=set_pk)
        questions = set.question_set.all()
        module = set.module
        return render(request, 'admin_set.html', {'set':set, 'questions':questions, 'module':module})

def add_set(request):
    if request.user.is_superuser:
        if request.method == "POST":
            name = request.POST.get('name', None)
            module_pk = request.POST.get('module_pk', None)
            if name and module_pk:
                print(name,module_pk)
                try:
                    module = Module.objects.get(pk=module_pk)
                except Module.DoesNotExist:
                    module = None
                if module is not None:
                    set = Set(name=name, module=module)
                    set.save()
                    return redirect('/modules/admin-panel/modules/'+str(module_pk)+'/sets')
        modules = Module.objects.all()
        return render(request, 'admin-add-set.html', {'modules':modules})
    return redirect('/admin-panel/')

def add_question(request, set_pk):
    if request.user.is_superuser:
        if request.is_ajax():
            ans_type = request.POST.get('ans_type', None)
            ans_text = request.POST.get('ans_text', None)
            dicom_file = request.FILES.get('dicom', None)
            set_pk = set_pk


            if ans_type and dicom_file:
                set = get_object_or_404(Set, pk=set_pk)
                if ans_type == "1":
                    question = Question(dcom_file=dicom_file, set=set, ans_type=1, ans_text=" ")
                    question.save()

                elif ans_type == "2":
                    if ans_text is not None:
                        question = Question(dcom_file=dicom_file, set=set, ans_type=2, ans_text=ans_text)
                        question.save()
                    else:
                        'please select the correct answer send warning by json'
                        pass

                return JsonResponse({'msg':'success'})
        else:
            set = get_object_or_404(Set, pk=set_pk)
            return render(request, 'admin_add_question.html', {'set':set})


def delete_set(request):
    if request.user.is_superuser:
        if request.is_ajax():
            set_pk = request.POST.get('set_pk', None)
            if set_pk:
                set = get_object_or_404(Set, pk=set_pk)
                set.delete()
                return JsonResponse({'msg':'success'})


def delete_question(request):
    if request.user.is_superuser:
        if request.is_ajax():
            q_pk = request.POST.get('question_pk', None)
            if q_pk:
                q = get_object_or_404(Question, pk=q_pk)
                q.delete()
                return JsonResponse({'msg':'success'})


def admin_attempted_sets(request):
    if request.user.is_superuser:
        attempted_setss = AttemptedSet.objects.all()
        return render(request, 'admin-attempted-sets.html', {'attempted_sets':attempted_setss})

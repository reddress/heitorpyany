from django.shortcuts import render

# Create your views here.
def main(request):
    output = {}
    if request.method == "POST":
        try:
            num = int(request.POST['num'])
            if num % 5 == 0 and num % 3 == 0:
                answer = "FizzBuzz"
            elif num % 5 == 0:
                answer = "Buzz"
            elif num % 3 == 0:
                answer = "Fizz"
            else:
                answer = num
        except:
            answer = "not a valid input"
        output['answer'] = answer
    return render(request, 'fizzbuzz/prompt.html', output)

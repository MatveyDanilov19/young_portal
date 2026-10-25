from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import DocumentSubmission, UserRating
from .forms import DocumentSubmissionForm

@login_required
def rating_dashboard(request):
    """Пункт 6 ТЗ: Рейтинг по итогам конкурса/курса"""
    rating, created = UserRating.objects.get_or_create(user=request.user)
    submissions = DocumentSubmission.objects.filter(user=request.user).order_by('-uploaded_at')
    
    return render(request, 'ratings/dashboard.html', {
        'rating': rating,
        'submissions': submissions
    })

@login_required
def upload_document(request):
    """Пункт 5 ТЗ: Автоматический подсчет баллов (база)"""
    if request.method == 'POST':
        form = DocumentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            
            # Логика начисления баллов (заглушка, которую ты позже усложнишь)
            # Например: сертификат = 10 баллов, диплом = 20 баллов
            score_map = {'cert': 10, 'diploma': 20, 'letter': 5, 'other': 2}
            submission.score_value = score_map.get(submission.document_type, 0)
            submission.save()
            
            # Обновляем общий рейтинг
            rating, _ = UserRating.objects.get_or_create(user=request.user)
            rating.total_score += submission.score_value
            rating.save()
            
            return redirect('ratings:dashboard')
    else:
        form = DocumentSubmissionForm()
        
    return render(request, 'ratings/upload.html', {'form': form})

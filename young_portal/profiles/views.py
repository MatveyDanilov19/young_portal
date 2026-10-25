from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserProfileForm

def profile_list(request):
    """Пункт 4 ТЗ: Справочник членов МС"""
    profiles = UserProfile.objects.select_related('user').all()
    return render(request, 'profiles/profile_list.html', {'profiles': profiles})

def profile_detail(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk)
    return render(request, 'profiles/profile_detail.html', {'profile': profile})

@login_required
def profile_edit(request):
    """Редактирование своего профиля"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profiles:profile_detail', pk=profile.pk)
    else:
        form = UserProfileForm(instance=profile)
        
    return render(request, 'profiles/profile_edit.html', {'form': form, 'profile': profile})

# 👇 ДОБАВЬ ЭТУ ФУНКЦИЮ
@login_required
def dashboard(request):
    """
    Личный кабинет. Просто перенаправляет на страницу профиля текущего пользователя.
    Это решает проблему NoReverseMatch и делает редирект после регистрации логичным.
    """
    # Получаем или создаем профиль для текущего юзера (на случай, если его ещё нет)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    # Перенаправляем на детальную страницу этого профиля
    return redirect('profiles:profile_detail', pk=profile.pk)
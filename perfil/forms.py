#-*- coding: utf-8 -*-
from django.template import RequestContext
from django.forms import ModelForm
from django import forms
from django.core import validators
from django.contrib.auth.models import User
from perfil.models import UserProfile


class RegistrationForm(ModelForm):
  username = forms.CharField(label='Usuário',widget = forms.TextInput(attrs = {'style':'height:auto'}), required=True)
  password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'id':'password','style':'height:auto'}))
  password2 = forms.CharField(label='Repita Senha', widget = forms.PasswordInput(attrs={'style':'height:auto'}))
  email = forms.EmailField(widget = forms.TextInput(attrs ={ 'id':'email', 'style':'height:auto'}), required=True)
  first_name = forms.CharField(label='Primeiro Nome',widget = forms.TextInput(attrs = {'id':'first_name', 'style':'height:auto'}), required=True)
  last_name = forms.CharField(label='Sobrenome',widget = forms.TextInput(attrs = {'id':'last_name', 'style':'height:auto'}), required=True)
  cpf = forms.CharField(label='CPF',widget = forms.TextInput(attrs = {'id':'cpf', 'style':'height:auto'}), required=True)
  image = forms.ImageField(label='Foto do Perfil',widget = forms.ClearableFileInput(attrs = {'id':'imagem', 'style':'height:auto'}), required=False)
  class Meta:
    model = UserProfile
    fields = ('username', 'first_name','last_name', 'password','password2', 'email' ,'cpf', 'cargo' ,'biografia', 'image')


  def clean_password2(self):
    password1 = self.cleaned_data.get("password","")
    password2 = self.cleaned_data['password2']
    if password1 != password2:
      raise forms.ValidationError("As senhas digitadas devem ser iguais para conferencia!")
    return password2

  def clean_username(self):
    data = self.cleaned_data.get('username',"")
    chars = set("0123456789!@#$%&*()_-+=`[]{}^~;:><,./?|\ºª  ,'")
    error = False
    if any((c in chars) for c in str(data)):
        raise forms.ValidationError("Tem Caracteres Invalidos!")
        error = True
    if error == False:
      try:
        User.objects.get(username=data)
      except User.DoesNotExist:
        return data
      raise forms.ValidationError("Usuário já existe.")
    return data

  def clean_email(self):
    data = self.cleaned_data.get('email',"")
    try:
      User.objects.get(email=data)
    except User.DoesNotExist:
      return data
    raise forms.ValidationError("Email já cadastrado.")

  def clean_cpf(self):    
    cpf = str(self.cleaned_data['cpf'])
    cpf = cpf.replace('.','')
    cpf = cpf.replace('-','')
    try:
      UserProfile.objects.get(cpf=int(cpf))
      error = 1
    except:
      error = 0

    if cpf == "00000000000" or cpf == "11111111111" or cpf == "22222222222" or cpf=="333333333333" or cpf == "44444444444" or cpf == "55555555555" or cpf == "66666666666" or cpf=="77777777777" or cpf=="88888888888" or cpf=="99999999999":
      error = 2
 
    i = 0
    multiplicador = 10
    somador = 0
    for i in range(9):
      somador = int(cpf[i])*multiplicador + somador
      multiplicador -= 1
      if (somador%11) < 2:
        d1 = 0
      else:
        d1 = 11 - (somador%11)
    if d1 != int(cpf[9]):
      error = 2
    i = 0
    multiplicador = 11
    somador = 0

    for i in range(10):
      somador = int(cpf[i])*multiplicador + somador
      multiplicador -= 1
      if (somador%11) < 2:
        d2 = 0
      else:
        d2 = 11 - (somador%11)

    if d2 != int(cpf[10]):
      error = 2
    
    if error == 1:
      raise forms.ValidationError("CPF já cadastrado.")    
    elif error == 2:
      raise forms.ValidationError("CPF Inválido.")
    else:
      return cpf  

class EditarForm(ModelForm):
  first_name = forms.CharField(label='Primeiro Nome',widget = forms.TextInput(attrs = {'id':'first_name', 'style':'height:auto'}), required=True)
  last_name = forms.CharField(label='Sobrenome',widget = forms.TextInput(attrs = {'id':'last_name', 'style':'height:auto'}), required=True)
  image = forms.ImageField(label='Foto do Perfil',widget = forms.ClearableFileInput(attrs = {'id':'imagem', 'style':'height:auto'}), required=False)
  class Meta:
    model = UserProfile
    fields = ('first_name','last_name', 'biografia' , 'image')


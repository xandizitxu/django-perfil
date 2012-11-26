#-*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from perfil.forms import RegistrationForm, EditarForm
from django.template import RequestContext
from perfil.models import UserProfile
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.utils.timezone import utc
import datetime

def index(request):
    if request.user.is_authenticated():
        login = User.objects.get(id=request.user.id)
    else:
        login = ""
    usuario = User.objects.order_by("id")
    usuario_extra = UserProfile.objects.all()
    return render_to_response('perfil/perfillista.html', {'login' : login, 'usuario_list' : usuario , 'usuario_extra_list' : usuario_extra } ,context_instance=RequestContext(request))

        
def registrar(request):
    if not request.user.is_authenticated():
        if request.method == 'POST': # If the form has been submitted...
            form = RegistrationForm(request.POST, request.FILES) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                username = request.POST['username']
                usuario = User.objects.create_user(username)
                usuario.is_active = False
                usuario.set_password(request.POST['password'])
                usuario.first_name =request.POST['first_name']
                usuario.last_name = request.POST['last_name']
                usuario.email =request.POST['email']
                usuario.save()
                usuario_extra = UserProfile(user=usuario)
                cpf = str(request.POST['cpf'])
                cpf = cpf.replace( ".", "" )
                cpf = cpf.replace( "-", "" )
                usuario_extra.cpf = cpf
                usuario_extra.cargo = request.POST['cargo']
                usuario_extra.biografia = request.POST['biografia']
                try:
                    photo = request.FILES['image'] 
                    filename = photo.name.replace(' ', '')
                    name = filename.split('.')
                    photo.name = username + "_" + str(datetime.datetime.now().strftime("%Y%m%dT%H%M%S")) + "_perfil." + name[len(name)-1]
                    imagem = usuario_extra.imagem.save(photo.name, ContentFile(photo.read()))
                    usuario_extra.save()
                except:
                    usuario_extra.save()
                return HttpResponseRedirect(reverse('perfil.views.sucesso', args=(username,)))
        else:
            form = RegistrationForm() # An unbound form#

        return render_to_response('perfil/registro.html', {
           'form': form,
        }, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')    	

def sucesso(request, username):
    try:
        user = User.objects.get(username = username)
        error = False
    except:
        error = True
    if error == False and user.is_active == True:
        return render_to_response('perfil/error.html', {'usuario' : user.username}, context_instance=RequestContext(request))
    elif error == True:
         return render_to_response('perfil/errorcadastro.html', context_instance=RequestContext(request))
    else:
        return render_to_response('perfil/sucesso.html', {
           'usuario': username,
        }, context_instance=RequestContext(request))    
def error(request):
        return HttpResponseRedirect('/')

def editar(request):
    username = User.objects.get(id=request.user.id)
    username_extra = UserProfile.objects.get(user_id=username.id)
    if request.method == 'POST': # If the form has been submitted...
        form = EditarForm(request.POST, request.FILES) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            username.last_name = request.POST['last_name']
            username.first_name = request.POST['first_name']
            username_extra.biografia = request.POST['biografia']

            if 'imagem-clear' in request.POST:
                username_extra.image = ""
            try: 
                photo = request.FILES['image'] 
                filename = photo.name.replace(' ', '')
                name = filename.split('.')
                photo.name = username.username + "_" + str(datetime.datetime.now().strftime("%Y%m%dT%H%M%S")) + "_perfil." + name[len(name)-1]
                imagem = username_extra.image.save(photo.name, ContentFile(photo.read()))
            except:
                nada = 1
            username.save()
            username_extra.save()
            return HttpResponseRedirect('/perfil/')
        else:
            form = EditarForm(initial={'first_name' : username.first_name, 'last_name' : username.last_name, 'biografia' : username_extra.biografia , 'image' : username_extra.image}) # An unbound form#

        return render_to_response('perfil/editar.html', {'login': username.username , 'form': form}, context_instance=RequestContext(request))
    else:
        form = EditarForm(initial={'first_name' : username.first_name, 'last_name' : username.last_name, 'biografia' : username_extra.biografia , 'image' : username_extra.image}) # An unbound form#

        return render_to_response('perfil/editar.html', {'login': username.username , 'form': form}, context_instance=RequestContext(request))

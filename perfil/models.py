from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.hashers import make_password
from filer.fields.image import FilerImageField
from django.core.files.storage import FileSystemStorage
from django.conf import settings

fs = FileSystemStorage(location=settings.MEDIA_ROOT)

class UserProfile(models.Model):
	user = models.OneToOneField(User,unique=True, primary_key=True, related_name="user")

	CARGO_CHOICE = (
	    (u'CV', u'Convidado'),
	    (u'AL', u'Aluno'),
	    (u'PR', u'Professor'),
	    (u'SR', u'Servidor'),
	)

	FUNCAO_CHOICE = (
	    (u'CO', u'Coordenador'),
	    (u'PE', u'Pesquisador/Desenvolvedor'),
	    (u'LI', u'Lider'),
	    (u'CR', u'Contribuidor'),
	)

	cpf = models.BigIntegerField()
	cargo = models.CharField(max_length=2, choices=CARGO_CHOICE)
	funcao = models.CharField(max_length=2, choices=FUNCAO_CHOICE)
	image = models.ImageField('Foto Perfil',storage = fs, upload_to="image/",blank=True)
	biografia = models.TextField(blank=True)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

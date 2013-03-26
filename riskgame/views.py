from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from django.forms import ModelForm
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from crispy_forms.bootstrap import FormActions

from riskgame.models import *

@login_required
def index(request):
    t = loader.get_template('riskgame/index.html')
    
    c = RequestContext(request, {
        'teams': Team.objects.all(),
        'create_team_form': CreateTeamform()
    })

    return HttpResponse(t.render(c))


def pre_launch(request):
    t = loader.get_template('riskgame/pre_launch.html')

    c = RequestContext(request, {
        'game': Game.objects.get_latest_game()
    })

    return HttpResponse(t.render(c))


class CreateTeamform(ModelForm):
    class Meta:
        model = Team
        fields = ('name', )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        self.helper.form_class = 'form'
        self.helper.form_action = reverse('team_create')
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('name', css_class='input-block-level', placeholder='Name'),
            FormActions(
                Submit('submit', 'Verzenden', css_class='btn')
            )
        )

        super(CreateTeamform, self).__init__(*args, **kwargs)

@login_required
def team_create(request):
    if request.method == "POST":
        name = request.POST.get('name', '')

        player = request.user.get_or_create_player()
        Team.objects.create(name=name, leader=player)

        return HttpResponseRedirect(reverse('index'))


class TeamDetail(DetailView):
    model = Team
    template_name = 'riskgame/team_detail.html'
    context_object_name = 'team'

@login_required
def request_team_join(request, pk):
    if request.method == "POST":
        player = request.user.get_or_create_player()
        team = Team.objects.get(id=pk)

        TeamJoinRequest.objects.create(team=team, player=player)

        return HttpResponse('join requested')

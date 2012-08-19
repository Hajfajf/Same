from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import util, template
from google.appengine.ext import db
from appengine_utilities import sessions
import datetime

class HomeHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('templates/home.html', locals()))

class AccountHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('templates/setup0.html', locals()))

class TeamHandler(webapp.RequestHandler):
    def get(self):
        session = sessions.Session()
        project = Project.get(session["ProjectID"])
        template_values = {
            'project': project,
         }
        self.response.out.write(template.render('templates/setup1.html', template_values))

class RatingHandler(webapp.RequestHandler):
    def get(self):
        session = sessions.Session()
        project = Project.get(session["ProjectID"])
        template_values = {
            'project': project,
         }
        self.response.out.write(template.render('templates/setup2.html', template_values))

class ScheduleHandler(webapp.RequestHandler):
    def get(self):
        session = sessions.Session()
        project = Project.get(session["ProjectID"])
        survey = Survey.get(session["SurveyID"])
        template_values = {
            'project': project,
            'survey' : survey,
         }
        self.response.out.write(template.render('templates/setup3.html', template_values))

class OverviewHandler(webapp.RequestHandler):
    def get(self):
        session = sessions.Session()
        project = Project.get(session["ProjectID"])
        survey = Survey.get(session["SurveyID"])
        template_values = {
            'project': project,
            'survey' : survey,
         }
        self.response.out.write(template.render('templates/setupconfirm.html', template_values))

class ConfirmHandler(webapp.RequestHandler):
    def get(self):
        session = sessions.Session()
        project = Project.get(session["ProjectID"])
        template_values = {
            'project': project,
         }
        self.response.out.write(template.render('templates/setupdone.html', template_values))

class ThermoHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('templates/thermo.html', locals()))

###Owner###
class Owner(db.Model):
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    company = db.StringProperty()
    department = db.StringProperty()
    project = db.StringProperty()
    project_key = db.StringProperty()
    email = db.EmailProperty()
    register_date = db.DateTimeProperty(auto_now_add=True)

###Project###
class Project(db.Model):
    name = db.StringProperty()
    company = db.StringProperty()
    department = db.StringProperty()
    member_nr = db.IntegerProperty()
    owner_name = db.StringProperty() 
    owner_key = db.StringProperty()
    survey_key = db.StringProperty()
    confirmed = db.BooleanProperty(default=False)
    register_date = db.DateTimeProperty(auto_now_add=True)


class OwnerAdd(webapp.RequestHandler):
    def post(self):
        session = sessions.Session()
        owner = Owner()
        project = Project()
        owner.first_name = str(self.request.get('first_name'))
        owner.last_name = str(self.request.get('last_name'))
        owner.company = str(self.request.get('company'))
        owner.department = str(self.request.get('department'))
        owner.project = str(self.request.get('project'))
        owner.email = self.request.get('email')
        owner.put()
        project.name = str(self.request.get('project'))
        project.company = str(self.request.get('company'))
        project.department = str(self.request.get('department'))
        project.owner_name = str(self.request.get('first_name')) + " " + str(self.request.get('last_name'))
        project.owner_key = str(owner.key())
        project.put()
        owner.project_key = str(project.key())
        owner.put()
        session["ProjectID"] = project.key() # sets keyname to value
        self.redirect('/setup-team')


###Set Team Members###
class TeamMember(db.Model):
    project = db.StringProperty()
    project_key = db.StringProperty()
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    email = db.EmailProperty()
    register_date = db.DateTimeProperty(auto_now_add=True)

class TeamAdd(webapp.RequestHandler):
    def post(self):
        session = sessions.Session()
        project = Project.get(session["ProjectID"])
        toprange = int(self.request.get('members'))
        project.member_nr = toprange- 1
        project.put()
        for i in range(1, toprange):
            member = TeamMember()
            member.project = str(self.request.get('project'))
            member.project_key = str(session["ProjectID"])
            member.first_name = str(self.request.get('tm%d_first_name' % i))
            member.last_name = str(self.request.get('tm%d_last_name' % i))
            member.email = self.request.get('tm%d_email' % i)
            member.put()
        self.redirect('/setup-ratings')

###Set Survey###
class Survey(db.Model):
    project = db.StringProperty()
    project_key = db.StringProperty()
    rt1_name = db.StringProperty()
    rt1_desc = db.StringProperty()
    rt2_name = db.StringProperty()
    rt2_desc = db.StringProperty()
    rt3_name = db.StringProperty()
    rt3_desc = db.StringProperty()
    rt4_name = db.StringProperty()
    rt4_desc = db.StringProperty()
    rt5_name = db.StringProperty()
    rt5_desc = db.StringProperty()
    rt6_name = db.StringProperty()
    rt6_desc = db.StringProperty()
    send_frequency = db.StringProperty()
    send_day = db.StringProperty()
    send_time = db.StringProperty()
    send_date = db.DateProperty(auto_now_add=True)
    confirmed = db.BooleanProperty(default=False)
    register_date = db.DateTimeProperty(auto_now_add=True)

class RatingAdd(webapp.RequestHandler):
    def post(self):
        session = sessions.Session()
        survey = Survey()
        project = Project.get(session["ProjectID"])
        survey.project = project.name
        survey.project_key = str(project.key())
        survey.rt1_name = str(self.request.get('rt1_name'))
        survey.rt1_desc = str(self.request.get('rt1_desc'))
        survey.rt2_name = str(self.request.get('rt2_name'))
        survey.rt2_desc = str(self.request.get('rt2_desc'))
        survey.rt3_name = str(self.request.get('rt3_name'))
        survey.rt3_desc = str(self.request.get('rt3_desc'))
        survey.rt4_name = str(self.request.get('rt4_name'))
        survey.rt4_desc = str(self.request.get('rt4_desc'))
        survey.rt5_name = str(self.request.get('rt5_name'))
        survey.rt5_desc = str(self.request.get('rt5_desc'))
        survey.rt6_name = str(self.request.get('rt6_name'))
        survey.rt6_desc = str(self.request.get('rt6_desc'))
        survey.put()
        session["SurveyID"] = survey.key() # sets keyname to value
        project.survey_key = str(session["SurveyID"])
        project.put()
        self.redirect('/setup-schedule')

###Set Schedule###
class ScheduleAdd(webapp.RequestHandler):
    def post(self):
        session = sessions.Session()
        survey = Survey.get(session["SurveyID"])
        survey.send_frequency = str(self.request.get('frequency'))
        survey.send_day = str(self.request.get('day'))
        survey.send_time = str(self.request.get('time'))
        #survey.send_date = str(self.request.get('send_date'))
        survey.put()
        self.redirect('/setup-overview')

###Confirm Survey###
class ConfirmSurvey(webapp.RequestHandler):
    def post(self):
        session = sessions.Session()
        survey = Survey.get(session["SurveyID"])
        project = Project.get(session["ProjectID"])
        survey.confirmed = bool('true')
        project.confirmed = bool('true')
        survey.put()
        project.put()
        self.redirect('/setup-confirmed')

def main():
    application = webapp.WSGIApplication([
        ('/', HomeHandler),
        ('/setup-account', AccountHandler),
        ('/scripts/owneradd', OwnerAdd),
        ('/setup-team', TeamHandler),
        ('/scripts/teamadd', TeamAdd),
        ('/setup-ratings', RatingHandler),
        ('/scripts/ratings', RatingAdd),
        ('/setup-schedule', ScheduleHandler),
        ('/scripts/schedule', ScheduleAdd),
        ('/setup-overview', OverviewHandler),
        ('/scripts/confirm', ConfirmSurvey),
        ('/setup-confirmed', ConfirmHandler),
        ('/thermo', ThermoHandler)], debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
  main()
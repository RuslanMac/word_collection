from app import application, db
from flask import render_template,flash,redirect, url_for, request, jsonify
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm, AddWordForm, EditProfileForm, DictionaryForm, NewsSearchForm
from app.models import User, Word, Language, Dictionary
from app.translate import translate
import random
from flask_babel import _

@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	NEWSAPI = application.config['NEWSAPI']
	form = NewsSearchForm()
	form.languages.choices = [('ru','Russian'), ('en', 'English'), ('it', 'Italian'), ('es', 'Spanish')]
	form.topic.choices = ['business', 'entertainment', 'general', 'health']
	newsapi = NEWSAPI.get_top_headlines(language = form.languages.data or 'ru')
	if form.validate_on_submit():
		newsapi = NEWSAPI.get_top_headlines(language = form.languages.data )
	return render_template('index.html', title='Home'  ,        user = current_user.username, form = form, newsapi = newsapi['articles'] )

@application.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash(_('Invalid username or password'))
			return redirect(url_for('login'))
		login_user(user, remember = form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html',title='Sign In',form=form)

@application.route('/register', methods = ['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	form.my_language.choices = [(language.id, language.language) for language in Language.query.all()]
	#form.languages.choices = [(language.id, language.language) for language in Language.query.all()]
	form.languages1.choices = [(language.id, language.language) for language in Language.query.all()]
	if form.validate_on_submit():
		if form.my_language.data in form.languages1.data:
			flash('Native language can not be a foreign language')
			return redirect(url_for('register'))
		language = Language.query.filter_by(id=form.my_language.data).first()	
		user = User(username = form.username.data, email=form.email.data, language_id=language.id)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		foreign_languages = form.languages1.data
		for foreign_language in foreign_languages:
			language = Language.query.filter_by(id=foreign_language).first()
			dictionary = Dictionary(user_id=user.id, language_id=language.id)
			db.session.add(dictionary)
			db.session.commit()
		flash(_('Congratulations, you are now a registered user!'))
		return redirect(url_for('login'))

	return render_template('register.html', title='Register', form = form)

@application.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@application.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)
	if form.validate_on_submit():
		if form.languages.data in current_user.languages:
			flash('The chosen language is alreay in learning')
		current_user.username = form.username.data
		db.session.commit()
		dictionary = Dictionary(user_id = currrent_user.id, language_id = form.languages.data)
		flash(_('Your changes have been saved!'))
		return redirect(url_for('edit_profile'))
	return render_template('edit_profile.html', title='Edit Profile', form = form)

@application.route('/search')
@login_required
def search():
	form = AddWordForm()
	dictionaries = current_user.languages
	languages_id = [language.language_id for language in dictionaries]
	languages = [Language.query.filter_by(id=language_id).first() for language_id in languages_id]
	form.languages.choices = [(language.id, language.language) for language in languages]
	return render_template('search.html', title = 'Search', form=form )

@application.route('/mywords', methods=['GET','POST'])
@login_required
def get_mywords():
	language_id = None
	dictionaryForm = DictionaryForm()
	dictionaries = current_user.languages
	#languages_id = [language.language_id for language in dictionaries]
	languages = [(dictionary.id, Language.query.filter_by(id=dictionary.language_id).first().language) for dictionary in dictionaries]
	#languages = [(Language.query.filter_by(id=language_id).first()) for language_id in languages_id]
	#kx = 75
	dictionaryForm.foreign_languages.choices = [language for language in languages]
	page = request.args.get('page', 1, type=int)
	if dictionaryForm.validate_on_submit():
		language_id = dictionaryForm.foreign_languages.data
	words = Dictionary.query.filter_by(id = language_id or 3).first().words.paginate(
		page, application.config['WORDS_PER_PAGE'], False)
	foreign_languages = current_user.languages
	next_url = url_for('mywords', page=words.next_num) \
	if words.has_next else None
	previous_url = url_for('mywords', page=words.prev_num) \
	if words.has_prev else None
	return render_template('mywords.html', title='Dictionary', words = words.items, next_url = next_url, previous_url = previous_url , form=dictionaryForm)

@application.route('/games')
@login_required
def games():
	return render_template('games.html',title = 'Games')

@application.route('/yes_not', methods=['GET', 'POST'])
@login_required
def yes_not():
	return render_template('game_yes_or_not.html', title = 'True or False Game')

@application.route('/test_api', methods=['GET', 'POST'])
@login_required
def test1x():
	form = NewsSearchForm()
	form.languages.choices = [('1', 'Russian'), ('2', 'English'), ('3', 'Italian'), ('4', 'Spanish')]
	form.topic.choices = [(1,'Auto'), (2, 'Politica'), (3, 'Economy'), (4, 'Sport')] 
	return render_template('test1x.html',     title='Test API', form=form) 




@application.route('/translate', methods=['POST'])
@login_required
def translate_text():
	return jsonify({'text': translate(request.form['text'],request.form['destLanguage'],request.form['sourceLanguage'] or Language.query.filter_by(id = current_user.language).first().lit)})         

@application.route('/add_word', methods=['POST'])
@login_required
def add_word():
	word = Word(native_language = request.form['text'],
				foreign_language= request.form['translation'], 
				dictionary_id =Dictionary.query.filter_by(language_id=Language.query.filter_by(lit=request.form['foreign_Language']).first().id).filter_by(user_id = current_user.id).first().id)
	db.session.add(word)
	db.session.commit()
	flash(_('The word has been added in the dictionary ! '))
	return render_template('search.html', title='Search')
 


@application.route('/get_words', methods=['POST', 'GET'])
@login_required
def get_words():
	languages = current_user.languages[0]
	words = [word for word in languages.words]
	count_words = len(words)
	new_words = []
	for k in range(0, count_words):
		answer=0
		i = random.randint(0, count_words-1)
		j = random.randint(0, count_words - 1)
		if i==j:
			answer=1
		else:
			answer=0
		word1 = {'foreign_language': words[i].foreign_language,
		 'native_language': words[j].native_language,
		 'native_language_true': words[i].native_language,
		 'answer': answer}
		new_words.append(word1)
	return jsonify({'words': new_words})      


	


@application.route('/get_next/', methods=['GET', 'POST'])
@login_required
def get_next():
	words = request.form['words']
	count_words = request.form['count_words']
	i = random.randint(0, count_words-1)
	j = random.randint(0, count_words - 1)
	answer = 1
	if i!=j:
		answer=0
	return jsonify({'words': {'foreign_language': words[i].foreign_language,
								'native_language': words[j].native_language,
								'native_langauge_true': words[i].native_language}}
					)


@application.route('/words_errors_collection', methods=['GET', 'POST'])
def get_words_errors():
	return render_template('words_errors.html', title='Words Errors')





@application.route('/initPage', methods=['POST','GET'])
@login_required
def initPage():
	languages = [{'en': 'English', 'ru': 'Russian', 'fr': 'French', 'it': 'Italian'}]
	return jsonify({'lang':languages})



@application.route('/get_languages/<learnings>', methods=['POST']) 
@login_required
def get_languages(learnings):
	if learnings == str(1):
		languages = [Language.query.filter_by(id = dictionary.language_id).first() for dictionary in current_user.languages]
		languages.append(Language.query.filter_by(id = current_user.language.id).first())
		languages = [{"id": language.lit, "language": language.language} for language in languages]
		
		return jsonify({'languages': languages})
	else:
		languages = Language.query.all()
		languages2 = [{"id": language.lit, "language": language.language} for language in languages]
		return jsonify({'languages': languages2})
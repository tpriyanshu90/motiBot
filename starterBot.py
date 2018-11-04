import os
import time
import re
from slackclient import SlackClient
import random
from translate import Translator

ISOLANGUAGES = [
      {"code":"ab","name":"Abkhaz","nativeName":"аҧсуа"},
      {"code":"aa","name":"Afar","nativeName":"Afaraf"},
      {"code":"af","name":"Afrikaans","nativeName":"Afrikaans"},
      {"code":"ak","name":"Akan","nativeName":"Akan"},
      {"code":"sq","name":"Albanian","nativeName":"Shqip"},
      {"code":"am","name":"Amharic","nativeName":"አማርኛ"},
      {"code":"ar","name":"Arabic","nativeName":"العربية"},
      {"code":"an","name":"Aragonese","nativeName":"Aragonés"},
      {"code":"hy","name":"Armenian","nativeName":"Հայերեն"},
      {"code":"as","name":"Assamese","nativeName":"অসমীয়া"},
      {"code":"av","name":"Avaric","nativeName":"авар мацӀ, магӀарул мацӀ"},
      {"code":"ae","name":"Avestan","nativeName":"avesta"},
      {"code":"ay","name":"Aymara","nativeName":"aymar aru"},
      {"code":"az","name":"Azerbaijani","nativeName":"azərbaycan dili"},
      {"code":"bm","name":"Bambara","nativeName":"bamanankan"},
      {"code":"ba","name":"Bashkir","nativeName":"башҡорт теле"},
      {"code":"eu","name":"Basque","nativeName":"euskara, euskera"},
      {"code":"be","name":"Belarusian","nativeName":"Беларуская"},
      {"code":"bn","name":"Bengali","nativeName":"বাংলা"},
      {"code":"bh","name":"Bihari","nativeName":"भोजपुरी"},
      {"code":"bi","name":"Bislama","nativeName":"Bislama"},
      {"code":"bs","name":"Bosnian","nativeName":"bosanski jezik"},
      {"code":"br","name":"Breton","nativeName":"brezhoneg"},
      {"code":"bg","name":"Bulgarian","nativeName":"български език"},
      {"code":"my","name":"Burmese","nativeName":"ဗမာစာ"},
      {"code":"ca","name":"Catalan; Valencian","nativeName":"Català"},
      {"code":"ch","name":"Chamorro","nativeName":"Chamoru"},
      {"code":"ce","name":"Chechen","nativeName":"нохчийн мотт"},
      {"code":"ny","name":"Chichewa; Chewa; Nyanja","nativeName":"chiCheŵa, chinyanja"},
      {"code":"zh","name":"Chinese","nativeName":"中文 (Zhōngwén), 汉语, 漢語"},
      {"code":"cv","name":"Chuvash","nativeName":"чӑваш чӗлхи"},
      {"code":"kw","name":"Cornish","nativeName":"Kernewek"},
      {"code":"co","name":"Corsican","nativeName":"corsu, lingua corsa"},
      {"code":"cr","name":"Cree","nativeName":"ᓀᐦᐃᔭᐍᐏᐣ"},
      {"code":"hr","name":"Croatian","nativeName":"hrvatski"},
      {"code":"cs","name":"Czech","nativeName":"česky, čeština"},
      {"code":"da","name":"Danish","nativeName":"dansk"},
      {"code":"dv","name":"Divehi; Dhivehi; Maldivian;","nativeName":"ދިވެހި"},
      {"code":"nl","name":"Dutch","nativeName":"Nederlands, Vlaams"},
      {"code":"en","name":"English","nativeName":"English"},
      {"code":"eo","name":"Esperanto","nativeName":"Esperanto"},
      {"code":"et","name":"Estonian","nativeName":"eesti, eesti keel"},
      {"code":"ee","name":"Ewe","nativeName":"Eʋegbe"},
      {"code":"fo","name":"Faroese","nativeName":"føroyskt"},
      {"code":"fj","name":"Fijian","nativeName":"vosa Vakaviti"},
      {"code":"fi","name":"Finnish","nativeName":"suomi, suomen kieli"},
      {"code":"fr","name":"French","nativeName":"français, langue française"},
      {"code":"ff","name":"Fula; Fulah; Pulaar; Pular","nativeName":"Fulfulde, Pulaar, Pular"},
      {"code":"gl","name":"Galician","nativeName":"Galego"},
      {"code":"ka","name":"Georgian","nativeName":"ქართული"},
      {"code":"de","name":"German","nativeName":"Deutsch"},
      {"code":"el","name":"Greek, Modern","nativeName":"Ελληνικά"},
      {"code":"gn","name":"Guaraní","nativeName":"Avañeẽ"},
      {"code":"gu","name":"Gujarati","nativeName":"ગુજરાતી"},
      {"code":"ht","name":"Haitian; Haitian Creole","nativeName":"Kreyòl ayisyen"},
      {"code":"ha","name":"Hausa","nativeName":"Hausa, هَوُسَ"},
      {"code":"he","name":"Hebrew (modern)","nativeName":"עברית"},
      {"code":"hz","name":"Herero","nativeName":"Otjiherero"},
      {"code":"hi","name":"Hindi","nativeName":"हिन्दी, हिंदी"},
      {"code":"ho","name":"Hiri Motu","nativeName":"Hiri Motu"},
      {"code":"hu","name":"Hungarian","nativeName":"Magyar"},
      {"code":"ia","name":"Interlingua","nativeName":"Interlingua"},
      {"code":"id","name":"Indonesian","nativeName":"Bahasa Indonesia"},
      {"code":"ie","name":"Interlingue","nativeName":"Originally called Occidental; then Interlingue after WWII"},
      {"code":"ga","name":"Irish","nativeName":"Gaeilge"},
      {"code":"ig","name":"Igbo","nativeName":"Asụsụ Igbo"},
      {"code":"ik","name":"Inupiaq","nativeName":"Iñupiaq, Iñupiatun"},
      {"code":"io","name":"Ido","nativeName":"Ido"},
      {"code":"is","name":"Icelandic","nativeName":"Íslenska"},
      {"code":"it","name":"Italian","nativeName":"Italiano"},
      {"code":"iu","name":"Inuktitut","nativeName":"ᐃᓄᒃᑎᑐᑦ"},
      {"code":"ja","name":"Japanese","nativeName":"日本語 (にほんご／にっぽんご)"},
      {"code":"jv","name":"Javanese","nativeName":"basa Jawa"},
      {"code":"kl","name":"Kalaallisut, Greenlandic","nativeName":"kalaallisut, kalaallit oqaasii"},
      {"code":"kn","name":"Kannada","nativeName":"ಕನ್ನಡ"},
      {"code":"kr","name":"Kanuri","nativeName":"Kanuri"},
      {"code":"ks","name":"Kashmiri","nativeName":"कश्मीरी, كشميري‎"},
      {"code":"kk","name":"Kazakh","nativeName":"Қазақ тілі"},
      {"code":"km","name":"Khmer","nativeName":"ភាសាខ្មែរ"},
      {"code":"ki","name":"Kikuyu, Gikuyu","nativeName":"Gĩkũyũ"},
      {"code":"rw","name":"Kinyarwanda","nativeName":"Ikinyarwanda"},
      {"code":"ky","name":"Kirghiz, Kyrgyz","nativeName":"кыргыз тили"},
      {"code":"kv","name":"Komi","nativeName":"коми кыв"},
      {"code":"kg","name":"Kongo","nativeName":"KiKongo"},
      {"code":"ko","name":"Korean","nativeName":"한국어 (韓國語), 조선말 (朝鮮語)"},
      {"code":"ku","name":"Kurdish","nativeName":"Kurdî, كوردی‎"},
      {"code":"kj","name":"Kwanyama, Kuanyama","nativeName":"Kuanyama"},
      {"code":"la","name":"Latin","nativeName":"latine, lingua latina"},
      {"code":"lb","name":"Luxembourgish, Letzeburgesch","nativeName":"Lëtzebuergesch"},
      {"code":"lg","name":"Luganda","nativeName":"Luganda"},
      {"code":"li","name":"Limburgish, Limburgan, Limburger","nativeName":"Limburgs"},
      {"code":"ln","name":"Lingala","nativeName":"Lingála"},
      {"code":"lo","name":"Lao","nativeName":"ພາສາລາວ"},
      {"code":"lt","name":"Lithuanian","nativeName":"lietuvių kalba"},
      {"code":"lu","name":"Luba-Katanga","nativeName":""},
      {"code":"lv","name":"Latvian","nativeName":"latviešu valoda"},
      {"code":"gv","name":"Manx","nativeName":"Gaelg, Gailck"},
      {"code":"mk","name":"Macedonian","nativeName":"македонски јазик"},
      {"code":"mg","name":"Malagasy","nativeName":"Malagasy fiteny"},
      {"code":"ms","name":"Malay","nativeName":"bahasa Melayu, بهاس ملايو‎"},
      {"code":"ml","name":"Malayalam","nativeName":"മലയാളം"},
      {"code":"mt","name":"Maltese","nativeName":"Malti"},
      {"code":"mi","name":"Māori","nativeName":"te reo Māori"},
      {"code":"mr","name":"Marathi (Marāṭhī)","nativeName":"मराठी"},
      {"code":"mh","name":"Marshallese","nativeName":"Kajin M̧ajeļ"},
      {"code":"mn","name":"Mongolian","nativeName":"монгол"},
      {"code":"na","name":"Nauru","nativeName":"Ekakairũ Naoero"},
      {"code":"nv","name":"Navajo, Navaho","nativeName":"Diné bizaad, Dinékʼehǰí"},
      {"code":"nb","name":"Norwegian Bokmål","nativeName":"Norsk bokmål"},
      {"code":"nd","name":"North Ndebele","nativeName":"isiNdebele"},
      {"code":"ne","name":"Nepali","nativeName":"नेपाली"},
      {"code":"ng","name":"Ndonga","nativeName":"Owambo"},
      {"code":"nn","name":"Norwegian Nynorsk","nativeName":"Norsk nynorsk"},
      {"code":"no","name":"Norwegian","nativeName":"Norsk"},
      {"code":"ii","name":"Nuosu","nativeName":"ꆈꌠ꒿ Nuosuhxop"},
      {"code":"nr","name":"South Ndebele","nativeName":"isiNdebele"},
      {"code":"oc","name":"Occitan","nativeName":"Occitan"},
      {"code":"oj","name":"Ojibwe, Ojibwa","nativeName":"ᐊᓂᔑᓈᐯᒧᐎᓐ"},
      {"code":"cu","name":"Old Church Slavonic, Church Slavic, Church Slavonic, Old Bulgarian, Old Slavonic","nativeName":"ѩзыкъ словѣньскъ"},
      {"code":"om","name":"Oromo","nativeName":"Afaan Oromoo"},
      {"code":"or","name":"Oriya","nativeName":"ଓଡ଼ିଆ"},
      {"code":"os","name":"Ossetian, Ossetic","nativeName":"ирон æвзаг"},
      {"code":"pa","name":"Panjabi, Punjabi","nativeName":"ਪੰਜਾਬੀ, پنجابی‎"},
      {"code":"pi","name":"Pāli","nativeName":"पाऴि"},
      {"code":"fa","name":"Persian","nativeName":"فارسی"},
      {"code":"pl","name":"Polish","nativeName":"polski"},
      {"code":"ps","name":"Pashto, Pushto","nativeName":"پښتو"},
      {"code":"pt","name":"Portuguese","nativeName":"Português"},
      {"code":"qu","name":"Quechua","nativeName":"Runa Simi, Kichwa"},
      {"code":"rm","name":"Romansh","nativeName":"rumantsch grischun"},
      {"code":"rn","name":"Kirundi","nativeName":"kiRundi"},
      {"code":"ro","name":"Romanian, Moldavian, Moldovan","nativeName":"română"},
      {"code":"ru","name":"Russian","nativeName":"русский язык"},
      {"code":"sa","name":"Sanskrit (Saṁskṛta)","nativeName":"संस्कृतम्"},
      {"code":"sc","name":"Sardinian","nativeName":"sardu"},
      {"code":"sd","name":"Sindhi","nativeName":"सिन्धी, سنڌي، سندھی‎"},
      {"code":"se","name":"Northern Sami","nativeName":"Davvisámegiella"},
      {"code":"sm","name":"Samoan","nativeName":"gagana faa Samoa"},
      {"code":"sg","name":"Sango","nativeName":"yângâ tî sängö"},
      {"code":"sr","name":"Serbian","nativeName":"српски језик"},
      {"code":"gd","name":"Scottish Gaelic; Gaelic","nativeName":"Gàidhlig"},
      {"code":"sn","name":"Shona","nativeName":"chiShona"},
      {"code":"si","name":"Sinhala, Sinhalese","nativeName":"සිංහල"},
      {"code":"sk","name":"Slovak","nativeName":"slovenčina"},
      {"code":"sl","name":"Slovene","nativeName":"slovenščina"},
      {"code":"so","name":"Somali","nativeName":"Soomaaliga, af Soomaali"},
      {"code":"st","name":"Southern Sotho","nativeName":"Sesotho"},
      {"code":"es","name":"Spanish","nativeName":"español, castellano"},
      {"code":"su","name":"Sundanese","nativeName":"Basa Sunda"},
      {"code":"sw","name":"Swahili","nativeName":"Kiswahili"},
      {"code":"ss","name":"Swati","nativeName":"SiSwati"},
      {"code":"sv","name":"Swedish","nativeName":"svenska"},
      {"code":"ta","name":"Tamil","nativeName":"தமிழ்"},
      {"code":"te","name":"Telugu","nativeName":"తెలుగు"},
      {"code":"tg","name":"Tajik","nativeName":"тоҷикӣ, toğikī, تاجیکی‎"},
      {"code":"th","name":"Thai","nativeName":"ไทย"},
      {"code":"ti","name":"Tigrinya","nativeName":"ትግርኛ"},
      {"code":"bo","name":"Tibetan Standard, Tibetan, Central","nativeName":"བོད་ཡིག"},
      {"code":"tk","name":"Turkmen","nativeName":"Türkmen, Түркмен"},
      {"code":"tl","name":"Tagalog","nativeName":"Wikang Tagalog, ᜏᜒᜃᜅ᜔ ᜆᜄᜎᜓᜄ᜔"},
      {"code":"tn","name":"Tswana","nativeName":"Setswana"},
      {"code":"to","name":"Tonga (Tonga Islands)","nativeName":"faka Tonga"},
      {"code":"tr","name":"Turkish","nativeName":"Türkçe"},
      {"code":"ts","name":"Tsonga","nativeName":"Xitsonga"},
      {"code":"tt","name":"Tatar","nativeName":"татарча, tatarça, تاتارچا‎"},
      {"code":"tw","name":"Twi","nativeName":"Twi"},
      {"code":"ty","name":"Tahitian","nativeName":"Reo Tahiti"},
      {"code":"ug","name":"Uighur, Uyghur","nativeName":"Uyƣurqə, ئۇيغۇرچە‎"},
      {"code":"uk","name":"Ukrainian","nativeName":"українська"},
      {"code":"ur","name":"Urdu","nativeName":"اردو"},
      {"code":"uz","name":"Uzbek","nativeName":"zbek, Ўзбек, أۇزبېك‎"},
      {"code":"ve","name":"Venda","nativeName":"Tshivenḓa"},
      {"code":"vi","name":"Vietnamese","nativeName":"Tiếng Việt"},
      {"code":"vo","name":"Volapük","nativeName":"Volapük"},
      {"code":"wa","name":"Walloon","nativeName":"Walon"},
      {"code":"cy","name":"Welsh","nativeName":"Cymraeg"},
      {"code":"wo","name":"Wolof","nativeName":"Wollof"},
      {"code":"fy","name":"Western Frisian","nativeName":"Frysk"},
      {"code":"xh","name":"Xhosa","nativeName":"isiXhosa"},
      {"code":"yi","name":"Yiddish","nativeName":"ייִדיש"},
      {"code":"yo","name":"Yoruba","nativeName":"Yorùbá"},
      {"code":"za","name":"Zhuang, Chuang","nativeName":"Saɯ cueŋƅ, Saw cuengh"}
    ]
# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM

GREETINGS = ['hola', 'hello', 'hi', 'Hi', 'hey!','hey',"What's up?"]
GREETING_RESPONSES = ["'sup bro", "hey", "hello my friend","all good"]
QUESTIONS = ['How are you?','How are you doing?']
QUESTIONS_RESPONSES = ["I'm fine what about you?","I'm fine","Great","Awesome"]
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
SET_OF_FUNCTIONS = ["Calculate","Translate"]

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def findISO(lang):
    for i in ISOLANGUAGES:
        if i["name"] == lang:
            return i["code"]
    return None

def handleFunction(command,func):
    """Function to calculate, Translate"""
    try:
        # re.search(r"(?i)"+func,' '.join(SET_OF_FUNCTIONS))
        if("calculate" == func.lower()):
            func,command = command.split()
            return eval(command)
        elif("translate" == func.lower()):
            command = re.split(r'\s',command)
            isoLan = findISO(command[len(command)-1])
            if isoLan == None:
                translation = "Sorry! we are unable to translate into this language"
                return translation
            translator= Translator(to_lang=isoLan)
            translation = translator.translate(' '.join(command[1:len(command)-2]))
            return translation
        else:
            return None
    except:
        return None

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(random.choice(GREETINGS))

    # Finds and executes the given command, filling in response
    response = None

    # This is where you start to implement more commands!

    # Code for Greetings
    if re.search(r"(?i)"+command,' '.join(GREETINGS)):
    	response = random.choice(GREETING_RESPONSES)

    # Code for QUESTIONS
    if re.search(r"(?i)"+command,' '.join(QUESTIONS)):
        response = random.choice(QUESTIONS_RESPONSES)

    # Performing various functions here
    func = re.split(r"\s",command)
    
    answer = None
    
    for i in SET_OF_FUNCTIONS:
        if(re.search(r"(?i)"+func[0],i)):
            answer = handleFunction(command,i)
            if answer:
                response = answer

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

#----------------------------------------MAIN PROGRAM---------------------------------------#
if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
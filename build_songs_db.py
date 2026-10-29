# -*- coding: utf-8 -*-
"""
Script to compile the VerseView-style Church Songs Database for ChurchView Projector.
Contains beloved Malayalam Christian Hymns & Songs (Kristheeya Keerthanangal, Athmeeya Geethangal)
with Malayalam script, Manglish transliteration, and English Hymns.
"""

import json
import os

songs = [
    {
        "id": 1,
        "number": 1,
        "category": "Cross & Redemption",
        "book": "Kristheeya Keerthanangal",
        "title_ml": "ക്രൂശിൻ നിഴലിൽ എനിക്കു",
        "title_en": "Krooshin Nizhalil Enikku",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "ക്രൂശിൻ നിഴലിൽ എനിക്കു - വൻ\nവിശ്രമ സ്ഥലം കണ്ടേൻ\nപാരിട മരുവിൽ ക്ഷീണിച്ചേർക്കും\nചാരുവാൻ ഒരു പാറ തൻ തണൽ",
                "en": "Krooshin nizhalil enikku - van\nVishrama sthalam kanden\nPaarida maruvil ksheenicherkkum\nChaaruvaan oru paara than thanal"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "യേശുവെൻ അഭയ സ്ഥാനം - എൻ\nസുരക്ഷിത സങ്കേതം\nപാപവും ശാപവും നീക്കി തന്ന\nപാപവിമോചന കാൽവരിയിൽ",
                "en": "Yeshuven abhaya sthaanam - en\nSurakshitha sanketham\nPaapavum shaapavum neekki thanna\nPaapavimochanam kaalvariyil"
            },
            {
                "label": "Stanza 2 / ചരണം 2",
                "tag": "S2",
                "ml": "കാൽവരി ക്രൂശിലെ രക്തം - എൻ\nപാപങ്ങൾ കഴുകിടുമേ\nജീവന്റെ ഉറവ ഒഴുകീടുന്നു\nതാഴ്മയായ് വന്നതിൻ അരികിൽ ഞാൻ",
                "en": "Kaalvari krooshile raktham - en\nPaapangal kazhukidume\nJeevante urava ozhukeedunnu\nThaazhmayaay vannathin arikil njan"
            },
            {
                "label": "Stanza 3 / ചരണം 3",
                "tag": "S3",
                "ml": "ക്രൂശേ എൻ ഏക പ്രശംസ - എൻ\nആനന്ദ കാരണം നീ\nയേശുവിൻ സ്നേഹം നിറഞ്ഞൊരു ക്രൂശേ\nആയുസ്സെല്ലാം നിന്നെ വാഴ്ത്തിടും ഞാൻ",
                "en": "Krooshe en eka prashamsa - en\nAananda kaaranam nee\nYeshuvin sneham niranjoru krooshe\nAayussellaam ninne vaazhthidum njan"
            }
        ]
    },
    {
        "id": 2,
        "number": 2,
        "category": "Love of God",
        "book": "Kristheeya Keerthanangal",
        "title_ml": "ദൈവത്തിന്റെ സ്നേഹം എത്രയോ ആശ്ചര്യം",
        "title_en": "Daivathinte Sneham Ethrayo Aascharyam",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "ദൈവത്തിന്റെ സ്നേഹം എത്രയോ ആശ്ചര്യം\nഅളപ്പാൻ അസാദ്ധ്യമേ\nആഴിയിൽ ആഴമേ വാഴ്ത്തുവിൻ സ്വർഗ്ഗമേ\nപാപിയെ വീണ്ടെടുത്ത സ്നേഹമേ",
                "en": "Daivathinte sneham ethrayo aascharyam\nAlappaan asaadhyame\nAazhiyil aazhame vaazhthuvin swargame\nPaapiye veendedutha snehame"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "മാനവ ചിന്തകൾക്കെല്ലാം അതീതമാം\nദൈവത്തിൻ ദിവ്യ സ്നേഹം\nഏകജാതൻ തന്ന ജീവനെ യാഗമായ്\nപാപികളാം നമുക്കായ് നൽകി അവൻ",
                "en": "Maanava chinthakalkkellaam atheethamaam\nDaivathin divya sneham\nEka jaathan thanna jeevane yaagamaay\nPaapikalaam namukkaay nalki avan"
            },
            {
                "label": "Stanza 2 / ചരണം 2",
                "tag": "S2",
                "ml": "സമുദ്രങ്ങൾ മുഴുവൻ മഷിയാക്കി മാറ്റിലും\nവാനമെല്ലാം കടലാസായ് തീരിലും\nദൈവത്തിൻ സ്നേഹത്തെ വർണ്ണിക്കാൻ നോക്കിലും\nതീരുകില്ലതു യുഗായുഗങ്ങളായ്",
                "en": "Samudrangal muzhuvan mashiyaakki maattilum\nVaanamellaam kadalaasaay theerilum\nDaivathin snehathe varnnikkaan nokkilum\nTheerukillathu yugaayugangalaay"
            },
            {
                "label": "Stanza 3 / ചരണം 3",
                "tag": "S3",
                "ml": "സ്വർഗ്ഗീയ സൈന്യങ്ങൾ വാഴ്ത്തി സ്തുതിക്കുന്നു\nനിത്യമാം സ്നേഹത്തെ താൻ\nരക്ഷകൻ യേശുവിൻ രക്തത്താൽ വീണ്ടെടുത്ത\nവിശുദ്ധന്മാരെല്ലാം ചേർന്നീടുമേ",
                "en": "Swargeeya sainyangal vaazhthi sthuthikkunnu\nNithyamaam snehathe thaan\nRakshakan Yeshuvin rakthathaal veendedutha\nVisudhanmaarellaam cherneedume"
            }
        ]
    },
    {
        "id": 3,
        "number": 3,
        "category": "Thanksgiving & Praise",
        "book": "Worship Songs",
        "title_ml": "നന്ദിയോടെ ഞാൻ സ്തുതി പാടിടും",
        "title_en": "Nandiyode Njan Sthuthi Paadidum",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "നന്ദിയോടെ ഞാൻ സ്തുതി പാടിടും\nഎന്റെ യേശു നാഥാ എനിക്കായ് നീ ചെയ്തൊരു\nനന്മകൾക്കൊന്നും പ്രതിനന്ദി ചെയ്യുവാൻ\nഒന്നുമില്ലെനിക്കായ് ഒന്നുമില്ലേ",
                "en": "Nandiyode njan sthuthi paadidum\nEnte Yeshu naathaa enikkaay nee cheythoru\nNanmakalkkonnum prathinandi cheyyuvaan\nOnnumillenikkaay onnumille"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "ജീവിത ഭാരത്താൽ തളർന്ന നേരം\nആശ്വാസമായി നീ അരികെ വന്നു\nകണ്ണീരൊപ്പി എന്നെ മാറോടണച്ചവൻ\nകരുതുന്ന ദിവ്യ സ്നേഹം ഓർത്തു ഞാൻ വാഴ്ത്തും",
                "en": "Jeevitha bhaarathaal thalarna neram\nAaswaasamaayi nee arike vannu\nKanneerroppi enne maarodanachavan\nKaruthunna divya sneham orthu njan vaazhthum"
            },
            {
                "label": "Stanza 2 / ചരണം 2",
                "tag": "S2",
                "ml": "അന്ധകാരത്തിൽ ഞാൻ നടന്നിടുമ്പോൾ\nപാതയിൽ വെളിച്ചമായ് മുൻപേ പോയി\nതകർന്ന മനസ്സോടെ കരഞ്ഞ നേരം\nതഴുകിയ സ്നേഹത്തിൻ കൈകളാൽ താങ്ങി",
                "en": "Andhakaarathil njan nadannidumbol\nPaathayil velichamaay munpe poyi\nThakarna manassode karanja neram\nThazhukiya snehathin kaigalaal thaangi"
            },
            {
                "label": "Stanza 3 / ചരണം 3",
                "tag": "S3",
                "ml": "ഈ നല്ല ജീവിതം തന്ന നാഥാ\nആയുസ്സു മുഴുവൻ നിനക്കായ് വാഴും\nദിവ്യമാം കൃപയാൽ എന്നെ നടത്തി\nനിത്യ വിശ്രമത്തിൽ എന്നെ നീ ചേർക്കും",
                "en": "Ee nalla jeevitham thanna naathaa\nAayussu muzhuvan ninakkaay vaazhum\nDivyamaam krupayaal enne nadathi\nNithya vishramathil enne nee cherkkum"
            }
        ]
    },
    {
        "id": 4,
        "number": 4,
        "category": "Trust & Faith",
        "book": "Kristheeya Keerthanangal",
        "title_ml": "യേശുവിൽ മാത്രം എന്റെ ആശ്രയം",
        "title_en": "Yeshuvil Mathram Ente Aashrayam (In Christ Alone)",
        "stanzas": [
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "യേശുവിൽ മാത്രം എന്റെ ആശ്രയം\nവെളിച്ചവും ജീവനും ശക്തിയും താൻ\nഅടിയുറച്ച പാറയാം ക്രിസ്തുവിൽ ഞാൻ\nകൊടുങ്കാറ്റിലും ഉറച്ചു നിൽക്കും",
                "en": "Yeshuvil maathram ente aashrayam\nVelichavum jeevanum shakthiyum thaan\nAdiyuracha paarayaam Kristhuvil njan\nKodungaattilum urachu nilkkum"
            },
            {
                "label": "Stanza 2 / ചരണം 2",
                "tag": "S2",
                "ml": "സ്നേഹത്തിൻ ഉയരം സമാധാനത്തിൻ ആഴം\nഭയങ്ങളും വ്യാകുലങ്ങളും അകലുമ്പോൾ\nഎൻ സാന്ത്വനദാതാവ് സർവ്വവും താൻ\nയേശുവിൻ സ്നേഹത്തിൽ ഞാൻ നിൽക്കുമേ",
                "en": "Snehathin uyaram samaadhaanathin aazham\nBhayangalum vyaakulangalum akalumbol\nEn saanthwanadaathaavu sarvvavum thaan\nYeshuvin snehathil njan nilkkume"
            },
            {
                "label": "Stanza 3 / ചരണം 3",
                "tag": "S3",
                "ml": "മണ്ണിൽ ശരീരം പൂകി കിടന്നു\nലോകത്തിൻ വെളിച്ചം ഇരുളിൽ മറഞ്ഞു\nപിന്നെ മഹത്വത്തോടുയർത്തെഴുന്നേറ്റു\nമരണത്തിൻ ശാപം നീക്കിക്കളഞ്ഞു",
                "en": "Mannil shareeram pooki kidannu\nLokathin velicham irulil maranju\nPinne mahathwathoduyarthezhunnettu\nMaranathin shaapam neekkikkalanju"
            },
            {
                "label": "Stanza 4 / ചരണം 4",
                "tag": "S4",
                "ml": "പാപത്തിൻ കുറ്റമില്ല മരണഭയമില്ല\nഇതാണ് ക്രിസ്തുവിൻ ജീവന്റെ ശക്തി\nജനനം മുതൽ അന്ത്യ ശ്വാസം വരെയും\nയേശുവെൻ ജീവിതം ഭരിച്ചിടുന്നു",
                "en": "Paapathin kuttamilla maranabhayamilla\nIthaanu Kristhuvin jeevante shakthi\nJananam muthal anthya shwaasam vareyum\nYeshuven jeevitham bharichidunnu"
            }
        ]
    },
    {
        "id": 5,
        "number": 5,
        "category": "Praise & Glory",
        "book": "Kristheeya Keerthanangal",
        "title_ml": "എന്റെ ദൈവമെന്റെ രക്ഷകൻ",
        "title_en": "Ente Daivamente Rakshakan",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "എന്റെ ദൈവമെന്റെ രക്ഷകൻ\nഎന്നെ കാക്കുന്നിതാ ദിനവും\nതന്റെ ചിറകിൻ കീഴിൽ സുരക്ഷിതനായ്\nഞാൻ വസിക്കുന്നു ശാന്തമായ്",
                "en": "Ente Daivamente rakshakan\nEnne kaakkunnithaa dinavum\nThante chirakin keezhil surakshithanaay\nNjan vasikkunnu shaanthamaay"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "അഗ്നിയിലൂടെ ഞാൻ കടന്നീടിലും\nതീ ജ്വാല എന്നെ ദഹിപ്പിക്കില്ല\nആഴിയലകൾ മേൽ ആഞ്ഞടിച്ചാലും\nതന്റെ കരം എന്നെ താങ്ങിടുമേ",
                "en": "Aagniyiloode njan kadanneedilum\nThee jwaala enne dahippikkilla\nAazhiyalakal mel aanjadichaalum\nThante karam enne thaangidume"
            },
            {
                "label": "Stanza 2 / ചരണം 2",
                "tag": "S2",
                "ml": "ആപത്തു നാളിൽ അവൻ എൻ കോട്ട\nസങ്കട വേളയിൽ ഉറ്റ തുണ\nഭയപ്പെടുകില്ല ഞാൻ ഭൂമി ഇളകിലും\nദൈവം എൻ ഉള്ളത്തിൽ വസിക്കയാൽ",
                "en": "Aapathu naalil avan en kotta\nSankada velayil utta thuna\nBhayappadukilla njan bhoomi ilakilum\nDaivam en ullathil vasikkayaal"
            }
        ]
    },
    {
        "id": 6,
        "number": 6,
        "category": "Goodness of God",
        "book": "Athmeeya Geethangal",
        "title_ml": "എത്ര നല്ലവൻ എന്റെ യേശു",
        "title_en": "Ethra Nallavan Ente Yeshu",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "എത്ര നല്ലവൻ എന്റെ യേശു താൻ\nഎത്ര വിശ്വസ്തൻ എന്റെ രക്ഷകൻ\nനാൾതോറും അവൻ തൻ കൃപ ചൊരിഞ്ഞു\nഎന്നെ നടത്തുന്നു ആനന്ദമായ്",
                "en": "Ethra nallavan ente Yeshu thaan\nEthra viswasthan ente rakshakan\nNaalthorum avan than krupa chorinju\nEnne nadathunnu aanandamaay"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "കൂരിരുൾ താഴ്‌വരയിൽ നടന്നാലും\nഒരു ഭയവും എന്നെ ബാധിക്കില്ല\nതന്റെ വടിയും കോലും എന്നെ\nതേറ്റുന്ന ദിവ്യമാം ആശ്വാസമായ്",
                "en": "Koorirul thaazhvarayil nadannaalum\nOru bhayavum enne baadhikkilla\nThante vadiyum kolum enne\nThettunna divyamaam aaswaasamaay"
            },
            {
                "label": "Stanza 2 / ചരണം 2",
                "tag": "S2",
                "ml": "ശത്രുക്കൾ കാൺകെ മേശ ഒരുക്കി\nഎന്റെ തല തൈലത്താൽ അഭിഷേകം ചെയ്തു\nഎന്റെ പാനപാത്രം കവിഞ്ഞൊഴുകുന്നു\nനന്മയും കൃപയും പിൻതുടരുമേ",
                "en": "Shathrukkal kaanke mesha orukki\nEnte thala thailathaal abhishekam cheythu\nEnte paanapaathram kavinjkozhukunnu\nNanmayum krupayum pinthudarume"
            }
        ]
    },
    {
        "id": 7,
        "number": 7,
        "category": "Psalms & Guidance",
        "book": "Kristheeya Keerthanangal",
        "title_ml": "യഹോവ എന്റെ ഇടയനാകുന്നു",
        "title_en": "Yahova Ente Idayanakunnu (Psalm 23)",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "യഹോവ എന്റെ ഇടയനാകുന്നു\nഎനിക്കൊന്നിനും കുറവുണ്ടാകില്ല\nപച്ചപ്പുൽപ്പുറങ്ങളിൽ എന്നെ അവൻ കിടത്തുന്നു\nശാന്ത ജലാശയ തീരങ്ങളിൽ നടത്തുന്നു",
                "en": "Yahova ente idayanakunnu\nEnikkonninum kuravundaakilla\nPachappulppurangalil enne avan kidathunnu\nShaantha jalaashaya theerangalil nadathunnu"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "എന്റെ പ്രാണനെ താൻ തണുപ്പിക്കുന്നു\nതന്റെ നാമത്തിൻ നിമിത്തമായ്\nനീതിയിൻ പാതയിൽ എന്നെ അവൻ\nനിത്യവും നടത്തുന്നു കൃപയോടെ",
                "en": "Ente praanane thaan thanuppikkunnu\nThante naamathin nimithamaay\nNeethiyin paathayil enne avan\nNithyavum nadathunnu krupayode"
            },
            {
                "label": "Stanza 2 / ചരണം 2",
                "tag": "S2",
                "ml": "മരണത്തിൻ നിഴലിൻ താഴ്‌വരയിൽ\nഞാൻ നടന്നീടിലും ഭയപ്പെടില്ല\nനീ എന്നോടുകൂടെ ഇരിക്കയാൽ\nനിൻ ദിവ്യ സന്നിധി എൻ ബലമേ",
                "en": "Maranathin nizhalin thaazhvarayil\nNjan nadanneedilum bhayappedilla\nNee ennodukoode irikkeyaal\nNin divya sannidhi en balame"
            }
        ]
    },
    {
        "id": 8,
        "number": 8,
        "category": "Love of Christ",
        "book": "Worship Songs",
        "title_ml": "അത്ഭുത സ്നേഹം ആശ്ചര്യ സ്നേഹം",
        "title_en": "Adbhutha Sneham Aascharya Sneham",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "അത്ഭുത സ്നേഹം ആശ്ചര്യ സ്നേഹം\nയേശുവേ നിൻ ദിവ്യ സ്നേഹം\nപാപിയാം എന്നെ സ്നേഹിപ്പാൻ തക്കവണ്ണം\nഞാൻ എന്തു നല്ലതു ചെയ്തു നാഥാ",
                "en": "Adbhutha sneham aascharya sneham\nYeshuve nin divya sneham\nPaapiyaam enne snehippaan thakkavannam\nNjan enthu nallathu cheythu naathaa"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "കാൽവരി കുന്നിൻ മുകളിൽ നീ എനിക്കായ്\nജീവനെ തന്നു പാപങ്ങൾ പോക്കി\nമുൾമുടി ചൂടിയ നിൻ ശിരസ്സതിൽ\nവഴിയുന്ന രക്തത്താൽ ശുദ്ധിയായി ഞാൻ",
                "en": "Kaalvari kunnin mukalil nee enikkaay\nJeevane thannu paapangal pokki\nMulmudi choodiya nin shirassathil\nVazhiyunna rakthathaal shudhiyaayi njan"
            },
            {
                "label": "Stanza 2 / ചരണം 2",
                "tag": "S2",
                "ml": "ലോകം തരുന്ന സ്നേഹങ്ങളെല്ലാം\nമാഞ്ഞുപോകുന്ന നിഴലുകൾ പോൽ\nമാറാത്ത സ്നേഹം യേശുവിൽ കണ്ടേൻ\nവാഴ്ത്തിടും ആയുസ്സിൻ നാളുകളൊക്കെയും",
                "en": "Lokam tharunna snehangalellaam\nMaanjupokunna nizhalukal pol\nMaaraatha sneham Yeshuvil kanden\nVaazhthidum aayussin naalukalokkeyum"
            }
        ]
    },
    {
        "id": 9,
        "number": 9,
        "category": "Praise & Worship",
        "book": "Kristheeya Keerthanangal",
        "title_ml": "സ്തുതിപ്പിൻ സ്തുതിപ്പിൻ യേശുദേവനെ",
        "title_en": "Sthuthippin Sthuthippin Yeshu Devane",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "സ്തുതിപ്പിൻ സ്തുതിപ്പിൻ യേശുദേവനെ\nഹല്ലേലൂയ്യാ പാടി വാഴ്ത്തുവിൻ\nതന്റെ അതിശയ പ്രവൃത്തികൾ ഓർത്തു\nആനന്ദത്തോടെന്നും സ്തുതിക്കുവിൻ",
                "en": "Sthuthippin sthuthippin Yeshu devane\nHalleluiah paadi vaazhthuvin\nThante athisaya pravarthikal orthu\nAanandathodennum sthuthikkuvin"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "പാപത്തിൽ ജീവിച്ച കാലമതിൽ\nസ്നേഹത്തിൻ കരം നീട്ടി വിളിച്ചവനാം\nശാപങ്ങൾ മാറ്റി സൗഖ്യവുമേകി\nസന്തോഷ തൈലത്താൽ പൂശിയവൻ",
                "en": "Paapathil jeevicha kaalamathil\nSnehathin karam neetti vilichavanaam\nShaapangal maatti saukhyavumeki\nSanthosha thailathaal pooshiyavan"
            },
            {
                "label": "Stanza 2 / ചരണം 2",
                "tag": "S2",
                "ml": "നമ്മുടെ ഭാരങ്ങൾ ചുമന്നവനാം\nനമ്മുടെ രോഗങ്ങൾ വഹിച്ചവനാം\nതന്റെ അടികളാൽ സൗഖ്യം ലഭിച്ചു\nസ്തുതിയിൻ യാഗങ്ങൾ അർപ്പിക്കുവിൻ",
                "en": "Nammude bhaarangal chumannavanaam\nNammude rogangal vahichavanaam\nThante adikalaal saukhyam labhichu\nSthuthiyin yaagangal arppikkuvin"
            }
        ]
    },
    {
        "id": 10,
        "number": 10,
        "category": "Hope & Comfort",
        "book": "Kristheeya Keerthanangal",
        "title_ml": "കഷ്ടങ്ങൾ നഷ്ടങ്ങൾ വന്നീടിലും",
        "title_en": "Kashtangal Nashtangal Vanneedilum",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "കഷ്ടങ്ങൾ നഷ്ടങ്ങൾ വന്നീടിലും\nകർത്താവിൻ സ്നേഹത്തിൽ നിന്നും എന്നെ\nവേർപിരിപ്പാൻ ആർക്കും സാധ്യമല്ല\nതൻ കൃപ എന്നുമെൻ ആശ്രയമേ",
                "en": "Kashtangal nashtangal vanneedilum\nKarthaavin snehathil ninnum enne\nVerpirippaan aarkkum saadhyamalla\nThan krupa ennumen aashrayame"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "ദാരിദ്ര്യമോ വിശപ്പോ പട്ടിണിയോ\nവാളോ ഉപദ്രവമോ മരണമോ\nജയാളിയായ് എന്നെ മാറ്റീടുന്നു\nസ്നേഹിച്ച രക്ഷകൻ യേശുവിലൂടെ",
                "en": "Daaridryamo vishappo pattiniyo\nVaalo upadravamo maranamo\nJayaaliyaay enne maatteedunnu\nSnehicha rakshakan Yeshuviloode"
            },
            {
                "label": "Stanza 2 / ചരണം 2",
                "tag": "S2",
                "ml": "ഉയരമോ ആഴമോ പ്രഭുത്വങ്ങളോ\nഇപ്പോഴുള്ളതോ വരുവാനുള്ളതോ\nദൈവത്തിൻ സ്നേഹത്തിൽ നിന്നും എന്നെ\nവേർതിരിക്കാൻ ഒന്നിനും ആകുകില്ല",
                "en": "Uyaramo aazhamo prabhuthwangalo\nIppozhullatho varuvaanullatho\nDaivathin snehathil ninnum enne\nVerthirikkaan onninum aakukilla"
            }
        ]
    },
    {
        "id": 11,
        "number": 11,
        "category": "Name of Jesus",
        "book": "Kristheeya Keerthanangal",
        "title_ml": "യേശുവിൻ നാമം അതിശയ നാമം",
        "title_en": "Yeshuvin Naamam Athisaya Naamam",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "യേശുവിൻ നാമം അതിശയ നാമം\nഭൂവിലുമേ സ്വർഗ്ഗത്തിലുമേ\nമറ്റൊരു നാമവുമില്ല രക്ഷക്കായി\nമഹിമയുള്ള നാമം യേശു നാമം",
                "en": "Yeshuvin naamam athisaya naamam\nBhoovilume swargathilume\nMattoru naamavumilla rakshakkaayi\nMahimayulla naamam Yeshu naamam"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "രോഗികൾ സൗഖ്യം പ്രാപിച്ചിടുന്നു\nബന്ധനങ്ങൾ തകർന്നു പോകുന്നു\nയേശുവിൻ നാമം ചൊല്ലിടുമ്പോൾ\nപിശാചുക്കൾ വിറച്ചോടീടുന്നു",
                "en": "Rogikal saukhyam praapichidunnu\nBandhanangal thakarnnu pokunnu\nYeshuvin naamam chollidumbol\nPishaachukkal virachodeedunnu"
            },
            {
                "label": "Stanza 2 / ചരണം 2",
                "tag": "S2",
                "ml": "മുട്ടുകൾ മടങ്ങും നാവുകൾ ഏറ്റുപറയും\nയേശുവെൻ കർത്താവെന്നു\nപിതാവാം ദൈവത്തിൻ മഹത്വത്തിനായി\nഎന്നേക്കും വാഴുന്ന നാമമതേ",
                "en": "Muttukal madangum naavukal ettuparayum\nYeshuven karthaavennu\nPithaavaam Daivathin mahathwathinaayi\nEnnekkum vaazhunna naamamathe"
            }
        ]
    },
    {
        "id": 12,
        "number": 12,
        "category": "Holy Spirit",
        "book": "Pentecostal Revival",
        "title_ml": "പരിശുദ്ധാത്മാവേ നിറയേണമേ",
        "title_en": "Parishudhatmave Nirayaname",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "പരിശുദ്ധാത്മാവേ നിറയേണമേ\nഅഗ്നിയായി എന്നിൽ ഇറങ്ങേണമേ\nപെന്തക്കോസ്ത് നാളിലെ ശക്തിയോടും\nഎന്നിൽ ഇന്നാത്മാവിൻ വർഷം പകരേണമേ",
                "en": "Parishudhatmave nirayaname\nAgniyaayi ennil iranganame\nPenthakosth naalile shakthiyodum\nEnnil innaathmaavin varsham pakaraname"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "ഉണർവ്വിൻ കാറ്റായി വീശേണമേ\nതണുത്ത ഹൃദയം ചൂടാക്കണമേ\nപുതിയ നാവിൽ ഞാൻ സ്തുതിച്ചിടുവാൻ\nഅഭിഷേക തൈലത്താൽ നിറയ്ക്കണമേ",
                "en": "Unarvvin kaattaayi veeshaname\nThanutha hrudhayam choodaakkaname\nPuthiya naavil njan sthuthichiduvaan\nAbhisheka thailathaal niraykkaname"
            },
            {
                "label": "Stanza 2 / ചരണം 2",
                "tag": "S2",
                "ml": "ദിവ്യ വരങ്ങളാൽ അലങ്കരിക്ക\nഫലങ്ങൾ എന്നിൽ കായ്പ്പതിനായ്\nയേശുവിൻ സാക്ഷിയായ് ജീവിച്ചിടാൻ\nആത്മശക്തിയോടെ എന്നെ അയയ്ക്കണമേ",
                "en": "Divya varangalaal alangarikka\nPhalangal ennil kaayppathinaay\nYeshuvin saakshiyaay jeevichidaan\nAathmashakthiyode enne ayaykkaname"
            }
        ]
    },
    {
        "id": 13,
        "number": 13,
        "category": "Prayer & Surrender",
        "book": "Kristheeya Keerthanangal",
        "title_ml": "സ്വർഗ്ഗീയ പിതാവേ നിൻ നാമം",
        "title_en": "Swargeeya Pithave Nin Namam",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "സ്വർഗ്ഗീയ പിതാവേ നിൻ നാമം\nഭൂമിയിലെങ്ങും വാഴ്ത്തപ്പെടേണമേ\nനിൻ രാജ്യം വേഗം വരേണമേ\nനിൻ ഹിതം ഭൂമിയിൽ നിറവേറണമേ",
                "en": "Swargeeya Pithaave nin naamam\nBhoomiyilengum vaazhthappedaname\nNin raajyam vegam varaname\nNin hitham bhoomiyil niraveraname"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "അന്നന്നുള്ള ആഹാരം നൽകണമേ\nകടങ്ങൾ ക്ഷമിക്കണമേ നാഥാ\nപരീക്ഷകളിൽ അകപ്പെടാതെ\nദുഷ്ടനിൽ നിന്നെന്നെ കാക്കണമേ",
                "en": "Annannulla aahaaram nalkaname\nKadangal kshamikkaname naathaa\nPareekshakalil akappadaathe\nDushtanil ninnenne kaakkaname"
            },
            {
                "label": "Stanza 2 / ചരണം 2",
                "tag": "S2",
                "ml": "രാജ്യവും ശക്തിയും മഹത്വവും\nഎന്നേക്കും നിനക്കുള്ളതല്ലോ\nനിത്യ പിതാവേ നിന്നെ വാഴ്ത്തും\nആമേൻ ഹല്ലേലൂയ്യാ ആമേൻ",
                "en": "Raajyavum shakthiyum mahathwavum\nEnnekkum ninakkullathallo\nNithya Pithaave ninne vaazhthum\nAamen Halleluiah Aamen"
            }
        ]
    },
    {
        "id": 14,
        "number": 14,
        "category": "Worship & Majesty",
        "book": "Worship Songs",
        "title_ml": "അങ്ങയെപ്പോലെ ആരുമില്ല",
        "title_en": "Angayeppole Aarumilla",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "അങ്ങയെപ്പോലെ ആരുമില്ല യേശുവേ\nസ്വർഗ്ഗത്തിലും ഭൂമിയിലുമേ\nഅതിശയങ്ങൾ ചെയ്യുന്ന ദൈവമേ\nആരാധന അങ്ങേയ്ക്കേ ആരാധന",
                "en": "Angayeppole aarumilla Yeshuve\nSwargathilum bhoomiyilume\nAthisayangal cheyyunna Daivame\nAaraadhana angeykke aaraadhana"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "അന്ധകാരത്തിൽ ജീവിച്ച എനിക്ക്\nനിത്യ പ്രകാശമായ് മാറി നീ നാഥാ\nതകർന്ന പാത്രമാം എന്നെ വീണ്ടും\nമേന്മയുള്ളൊരു പാത്രമായ് തീർത്തു നീ",
                "en": "Andhakaarathil jeevicha enikku\nNithya prakaashamaay maari nee naathaa\nThakarna paathramaam enne veendum\nMenmayulloru paathramaay theerthu nee"
            },
            {
                "label": "Stanza 2 / ചരണം 2",
                "tag": "S2",
                "ml": "എന്റെ ബലഹീനതകളിൽ നിൻ കൃപ\nതികഞ്ഞു വരുന്നു എൻ രക്ഷകനേ\nനിന്റെ നാമത്തിൽ ഞാൻ ആശ്രയിക്കും\nജീവനുള്ള നാളൊക്കെയും വാഴ്ത്തും ഞാൻ",
                "en": "Ente balaheenathakalil nin krupa\nThikanju varunnu en rakshakane\nNinte naamathil njan aashrayikkum\nJeevanulla naalokkeyum vaazhthum njan"
            }
        ]
    },
    {
        "id": 15,
        "number": 15,
        "category": "Peace & Comfort",
        "book": "Kristheeya Keerthanangal",
        "title_ml": "ശാന്തി നൽകും ദൈവമേ",
        "title_en": "Shanthi Nalkum Daivame",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "ശാന്തി നൽകും ദൈവമേ നിന്റെ\nസന്നിധി എത്രയോ മനോഹരം\nലോകാശ്വാസം മാഞ്ഞു പോകുമ്പോൾ\nദൈവീക ശാന്തി എന്നിൽ നിറയുന്നു",
                "en": "Shanthi nalkum Daivame ninte\nSannidhi ethrayo manoharam\nLokaaswaasam maanju pokumbol\nDaiveeka shanthi ennil nirayunnu"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "എന്റെ ചിന്തകളിൽ സമാധാനമേകി\nആകുലതകൾ നീക്കിക്കളഞ്ഞു\nകർത്താവേ നിന്റെ തിരുസാന്നിധ്യം\nസന്തോഷത്തിന്റെ പൂർണ്ണതയല്ലോ",
                "en": "Ente chinthakalil samaadhaananeki\nAakulathakal neekkikkalanju\nKarthaave ninte thirusaannidhyam\nSanthoshathinte poornnathayallo"
            }
        ]
    },
    {
        "id": 16,
        "number": 16,
        "category": "Grace",
        "book": "Worship Songs",
        "title_ml": "നിൻ കൃപയെനിക്ക് മതി യേശുവേ",
        "title_en": "Nin Krupoyenikku Mathi Yeshuve",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "നിൻ കൃപയെനിക്ക് മതി യേശുവേ\nഈ മരുഭൂമി യാത്രയിലുടനീളം\nഎന്റെ ബലഹീനതയിൽ നിൻ ശക്തി\nതികഞ്ഞുവരുന്നതാൽ നന്ദി ചൊല്ലും",
                "en": "Nin krupoyenikku mathi Yeshuve\nEe marubhoomi yaathrayiludaneelam\nEnte balaheenathayil nin shakthi\nThikanjuvarunnathaal nandi chollum"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "ശത്രുവിൻ മുമ്പിൽ പതറാതെ നിൽക്കാൻ\nദിവ്യ കൃപ എന്നെ സഹായിക്കുന്നു\nതോളിൽ ചുമക്കും ഇടയൻ നീയെൻ\nആയുസ്സെല്ലാം നിന്നെ അനുഗമിക്കും",
                "en": "Shathruvin mumpil patharaathe nilkkaan\nDivya krupa enne sahaayikkunnu\nTholil chumakkum idayan neeyen\nAayussellaam ninne anugamikkum"
            }
        ]
    },
    {
        "id": 17,
        "number": 17,
        "category": "Comfort & Peace",
        "book": "Kristheeya Keerthanangal",
        "title_ml": "മാനസമേ ശാന്തമാക",
        "title_en": "Manasame Shanthamaka",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "മാനസമേ ശാന്തമാക\nയേശുവിൽ പൂർണ്ണമായ് ചാരിടുക\nലോകത്തിൻ ഭാരങ്ങൾ ഒക്കെയും അവൻ\nതോളിൽ ചുമക്കും വിശ്വസ്തനായ്",
                "en": "Maanasame shaanthamaaka\nYeshuvil poornnamaay chaariduka\nLokathin bhaarangal okkeyum avan\nTholil chumakkum viswasthanaay"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "കടലലകൾ ആഞ്ഞടിച്ചാലും\nതോണി മുങ്ങാൻ പോകിലും\nകാറ്റിനെയും കടലിനെയും ശാസിക്കും\nരക്ഷകൻ യേശു നിന്നരികിലുണ്ട്",
                "en": "Kadalalakal aanjadichaalum\nThoni mungaan pokilum\nKaattineyum kadalineyum shaasikkum\nRakshakan Yeshu ninnarikilundu"
            }
        ]
    },
    {
        "id": 18,
        "number": 18,
        "category": "Praise & Worship",
        "book": "Worship Songs",
        "title_ml": "സ്തുതികൾക്ക് യോഗ്യനേ ആരാധന",
        "title_en": "Sthuthikalkku Yogyane Aaradhana",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "സ്തുതികൾക്ക് യോഗ്യനേ ആരാധന\nമഹിമയും പുകഴ്ചയും അങ്ങേയ്ക്കല്ലോ\nദൈവമേ നീ എത്ര പരിശുദ്ധൻ\nനിത്യപിതാവേ ആരാധന",
                "en": "Sthuthikalkku yogyane aaraadhana\nMahimayum pukazhchayum angeykkallo\nDaivame nee ethra parishuddhan\nNithyapithaave aaraadhana"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "കരങ്ങൾ ഉയർത്തി ഞാൻ വാഴ്ത്തീടുന്നു\nഹൃദയം തുറന്നു പുകഴ്ത്തീടുന്നു\nയേശുവേ അങ്ങേയ്ക്കായ് ജീവിക്കും ഞാൻ\nഎന്നുമെന്നും അങ്ങേ സാക്ഷിയായ്",
                "en": "Karangal uyarthi njan vaazhtheedunnu\nHrudhayam thurannu pukazhtheedunnu\nYeshuve angeykkaay jeevikkum njan\nEnnumennum angey saakshiyaay"
            }
        ]
    },
    {
        "id": 19,
        "number": 19,
        "category": "Cross & Blood",
        "book": "Kristheeya Keerthanangal",
        "title_ml": "കാൽവരി ക്രൂശിലെ യാഗമതേ",
        "title_en": "Kalvari Krooshile Yagamathae",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "കാൽവരി ക്രൂശിലെ യാഗമതേ\nപാപ പരിഹാര രക്തമതേ\nക്രിസ്തുവിൻ ജീവത്യാഗത്താലെൻ\nപാപങ്ങൾ പോക്കി സ്വതന്ത്രനായ്",
                "en": "Kaalvari krooshile yaagamathe\nPaapa parihaara rakthamathe\nKristhuvin jeevathyaagathaalen\nPaapangal pokki swathanthranaay"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "കുറ്റങ്ങൾ നീക്കി ശാപങ്ങൾ മാറ്റി\nനീതിമാനാക്കി തൻ രക്തത്താൽ\nനിത്യജീവൻ എനിക്കായ് തന്നോൻ\nയേശുവെൻ പ്രാണപ്രിയനല്ലോ",
                "en": "Kuttangal neekki shaapangal maatti\nNeethimaanaakki than rakthathaal\nNithyajeevan enikkaay thannon\nYeshuven praanapriyanallo"
            }
        ]
    },
    {
        "id": 20,
        "number": 20,
        "category": "Communion & Bread of Life",
        "book": "Athmeeya Geethangal",
        "title_ml": "ജീവന്റെ അപ്പമേ എന്നിലേക്ക് വരിക",
        "title_en": "Jeevante Appame Ennilekku Varika",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "ജീവന്റെ അപ്പമേ എന്നിലേക്ക് വരിക\nആത്മാവിൻ ദാഹം തീർത്തു തരിക\nനിത്യ ജീവൻ പകരുന്ന ദിവ്യ രക്തമേ\nഎന്നിൽ ഒഴുകി വിശുദ്ധനാക്കുക",
                "en": "Jeevante appame ennilekku varika\nAathmaavin daaham theerthu tharika\nNithya jeevan pakarunna divya rakthame\nEnnil ozhuki visuddhanaakkuka"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "കർത്താവിൻ തിരുമേനി ഞങ്ങൾക്കായി നുറുങ്ങി\nക്രിസ്തുവിൻ രക്തം ഞങ്ങൾക്കായി ചിന്തി\nമേശയിങ്കൽ വന്നിതാ നന്ദിയോടെ ഞങ്ങൾ\nതിരുസാന്നിധ്യത്തിൽ താണു വണങ്ങുന്നു",
                "en": "Karthaavin thirumeni njangalkkaayi nurungi\nKristhuvin raktham njangalkkaayi chinthi\nMeshayinkal vannithaa nandiyode njangal\nThirusaannidhyathil thaanu vanangunnu"
            }
        ]
    },
    {
        "id": 21,
        "number": 21,
        "category": "Faithfulness",
        "book": "Worship Songs",
        "title_ml": "വിശ്വസ്ത ദൈവമേ നിൻ സ്നേഹം",
        "title_en": "Viswastha Daivame Nin Sneham",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "വിശ്വസ്ത ദൈവമേ നിൻ സ്നേഹം\nപ്രഭാതം തോറും പുതിയതല്ലോ\nനിന്റെ വിശ്വസ്തത എത്രയോ വലിയത്\nഎന്റെ ആശ്രയം നീ മാത്രമെ",
                "en": "Viswastha Daivame nin sneham\nPrabhaatham thorum puthiyathallo\nNinte viswasthatha ethrayo valiyathu\nEnte aashrayam nee maathrame"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "മനുഷ്യർ കൈവിട്ട നേരത്തും\nകൈവിടാതെ എന്നെ കാത്തവൻ നീ\nവാക്കു മാറാത്ത വാഗ്ദത്ത നാഥാ\nനിന്റെ നാമത്തെ ഞാൻ പുകഴ്ത്തും",
                "en": "Manushyar kaivitta nerathum\nKaividaathe enne kaathavan nee\nVaakku maaraatha vaagdatha naathaa\nNinte naamathe njan pukazhthum"
            }
        ]
    },
    {
        "id": 22,
        "number": 22,
        "category": "Grace & Mercy",
        "book": "Kristheeya Keerthanangal",
        "title_ml": "ദൈവമേ നിന്റെ കൃപയാൽ",
        "title_en": "Daivame Ninte Krupayaal",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "ദൈവമേ നിന്റെ കൃപയാൽ ഞാൻ\nഇന്നുവരെയും ജീവിക്കുന്നു\nനിന്റെ മഹാദയ ഒന്നു കൊണ്ടുമാത്രം\nഞാൻ മുടിഞ്ഞു പോകാതിരുന്നു",
                "en": "Daivame ninte krupayaal njan\nInnuvareyum jeevikkunnu\nNinte mahaadaya onnu kondumaathram\nNjan mudinju pokaathirunnu"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "എന്റെ യോഗ്യതയല്ല നിൻ കൃപയല്ലോ\nഎന്നെ ഈ നിലയിൽ ആക്കിയതും\nനിന്റെ ചിറകിൻ നിഴലിൽ പാർക്കാൻ\nഇടയാക്കിയ നാഥനെ സ്തുതിക്കും",
                "en": "Ente yogyathayalla nin krupayallo\nEnne ee nilayil aakkiyathum\nNinte chirakin nizhalil paarkkaan\nIdayaakkiya naathane sthuthikkum"
            }
        ]
    },
    {
        "id": 23,
        "number": 23,
        "category": "Praise & Blessings",
        "book": "Kristheeya Keerthanangal",
        "title_ml": "എന്റെ ആത്മാവേ യഹോവയെ വാഴ്ത്തുക",
        "title_en": "Ente Aathmave Yahovaye Vazhthuka (Psalm 103)",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "എന്റെ ആത്മാവേ യഹോവയെ വാഴ്ത്തുക\nഎന്റെ ഉള്ളമേ തൻ വിശുദ്ധ നാമത്തെ\nതാൻ ചെയ്ത ഉപകാരങ്ങൾ ഒന്നുമേ\nമറക്കാതെ വാഴ്ത്തുക ആനന്ദമായ്",
                "en": "Ente aathmave Yahovaye vaazhthuka\nEnte ullame than visuddha naamathe\nThaan cheytha upakaarangal onnume\nMarakkaathe vaazhthuka aanandamaay"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "നിന്റെ അകൃത്യങ്ങളൊക്കെയും ക്ഷമിക്കുന്നു\nനിന്റെ രോഗങ്ങളൊക്കെയും സൗഖ്യമാക്കുന്നു\nനിന്റെ ജീവനെ കുഴിയിൽ നിന്നവൻ വീണ്ടെടുത്ത്\nദയയും കരുണയും അണിയിക്കുന്നു",
                "en": "Ninte akruthyangalokkeyum kshamikkunnu\nNinte rogangalokkeyum saukhyamaakkunnu\nNinte jeevane kuzhiyil ninnavan veendeduthu\nDayayum karunayum aniyikkunnu"
            }
        ]
    },
    {
        "id": 24,
        "number": 24,
        "category": "Dedication",
        "book": "Kristheeya Keerthanangal",
        "title_ml": "കർത്താവേ നിന്റെ തിരുപാദത്തിൽ",
        "title_en": "Karthave Ninte Thirupaadathil",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "കർത്താവേ നിന്റെ തിരുപാദത്തിൽ\nഎന്നെത്തന്നെ ഞാൻ സമർപ്പിക്കുന്നു\nഎന്റെ ജീവിതം നിനക്കായ് വാഴുവാൻ\nനിൻ ദിവ്യ കരം എന്നെ നയിക്കണമേ",
                "en": "Karthaave ninte thirupaadathil\nEnnethanne njan samarppikkunnu\nEnte jeevitham ninakkaay vaazhuvaan\nNin divya karam enne nayikkaname"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "എന്റെ മനസ്സും എന്റെ ശരീരവും\nസജീവയജ്ഞമായ് അർപ്പിക്കുന്നു\nലോകത്തിൻ മോഹങ്ങൾ വെടിഞ്ഞു ഞാൻ\nനിന്റെ ഇഷ്ടം നിറവേറ്റിടും",
                "en": "Ente manassum ente shareeravum\nSajeevayajnamaay arppikkunnu\nLokathin mohangal vedinju njan\nNinte ishtam niraverttidum"
            }
        ]
    },
    {
        "id": 25,
        "number": 25,
        "category": "Calvary Love",
        "book": "Kristheeya Keerthanangal",
        "title_ml": "കാൽവരിയിലെ ദിവ്യ സ്നേഹം",
        "title_en": "Kalvariyile Divya Sneham",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "കാൽവരിയിലെ ദിവ്യ സ്നേഹം\nഓർത്തു ഞാൻ കണ്ണീരൊഴുക്കുന്നു\nനിഷ്കളങ്കമാം കുഞ്ഞാടവൻ\nക്രൂശിൽ പ്രാണനെ വെടിഞ്ഞുവല്ലോ",
                "en": "Kaalvariyile divya sneham\nOrthu njan kanneerozhukkunnu\nNishkalankamaam kunjaadavan\nKrooshil praanane vedinjuvallo"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "എന്റെ പാപത്തിൻ ശിക്ഷയെല്ലാം\nതന്റെ മേലവൻ ഏറ്റു വാങ്ങി\nതന്റെ മുറിവുകളാൽ സൗഖ്യമേകി\nനിത്യ രക്ഷയൊരുക്കി തന്നവൻ",
                "en": "Ente paapathin shikshayellaam\nThante melavan ettu vaangi\nThante murivukalaal saukhyameki\nNithya rakshayorukki thannavan"
            }
        ]
    },
    # ENGLISH HYMNS (Beloved in Church of God & Kerala Congregations)
    {
        "id": 31,
        "number": 31,
        "category": "English Hymns",
        "book": "Hymns of Faith",
        "title_ml": "അത്ഭുത കൃപ (Amazing Grace)",
        "title_en": "Amazing Grace",
        "stanzas": [
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "അത്ഭുത കൃപ! എത്ര മധുര ശബ്ദം\nഎന്നെപ്പോൽ ഒരു പാപിയെ രക്ഷിച്ചു!\nഞാൻ ഒരിക്കൽ നഷ്ടപ്പെട്ടു, എന്നാൽ ഇപ്പോൾ കണ്ടെത്തി;\nഅന്ധനായിരുന്നു ഞാൻ, ഇപ്പോൾ കാണുന്നു.",
                "en": "Amazing grace! How sweet the sound\nThat saved a wretch like me!\nI once was lost, but now am found;\nWas blind, but now I see."
            },
            {
                "label": "Stanza 2 / ചരണം 2",
                "tag": "S2",
                "ml": "കൃപയാണ് എന്റെ ഹൃദയത്തെ ഭയപ്പെടുത്താൻ പഠിപ്പിച്ചത്,\nകൃപയാണ് എന്റെ ഭയങ്ങളെ ശമിപ്പിച്ചത്;\nഞാൻ ആദ്യം വിശ്വസിച്ച ആ നാഴികയിൽ\nആ കൃപ എത്ര വിലപ്പെട്ടതായി തോന്നി!",
                "en": "'Twas grace that taught my heart to fear,\nAnd grace my fears relieved;\nHow precious did that grace appear\nThe hour I first believed."
            },
            {
                "label": "Stanza 3 / ചരണം 3",
                "tag": "S3",
                "ml": "അനേകം ആപത്തുകളിലൂടെയും പ്രയാസങ്ങളിലൂടെയും\nഞാൻ ഇതിനകം കടന്നുവന്നു;\nകൃപയാണ് എന്നെ ഇതുവരെ സുരക്ഷിതമായി കൊണ്ടുവന്നത്,\nകൃപ എന്നെ വീട്ടിലേക്ക് നയിക്കും.",
                "en": "Through many dangers, toils, and snares,\nI have already come;\n'Tis grace hath brought me safe thus far,\nAnd grace will lead me home."
            },
            {
                "label": "Stanza 4 / ചരണം 4",
                "tag": "S4",
                "ml": "നാം പതിനായിരം വർഷങ്ങൾ അവിടെ ആയിരുന്നാലും,\nസൂര്യനെപ്പോലെ ശോഭിച്ചുകൊണ്ട്,\nദൈവത്തിന്റെ സ്തുതി പാടുവാൻ ഉള്ള ദിനങ്ങൾ\nതുടങ്ങിയ നാളിനേക്കാൾ ഒട്ടും കുറവല്ല.",
                "en": "When we've been there ten thousand years,\nBright shining as the sun,\nWe've no less days to sing God's praise\nThan when we'd first begun."
            }
        ]
    },
    {
        "id": 32,
        "number": 32,
        "category": "English Hymns",
        "book": "Hymns of Faith",
        "title_ml": "എന്റെ കർത്താവേ ദൈവമേ (How Great Thou Art)",
        "title_en": "How Great Thou Art",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "അപ്പോൾ എൻ ആത്മാവു പാടുന്നു രക്ഷകാ,\nനീ എത്ര വലിയവൻ! നീ എത്ര വലിയവൻ!\nഅപ്പോൾ എൻ ആത്മാവു പാടുന്നു രക്ഷകാ,\nനീ എത്ര വലിയവൻ! നീ എത്ര വലിയവൻ!",
                "en": "Then sings my soul, my Saviour God, to Thee:\nHow great Thou art, how great Thou art!\nThen sings my soul, my Saviour God, to Thee:\nHow great Thou art, how great Thou art!"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "ഓ കർത്താവേ ദൈവമേ! വിസ്മയത്തോടെ ഞാൻ\nനിൻ കരങ്ങൾ തീർത്ത പ്രപഞ്ചം കാണുമ്പോൾ,\nനക്ഷത്രങ്ങളെ കാണുന്നു, ഗർജ്ജിക്കുന്ന ഇടിമുഴക്കം കേൾക്കുന്നു,\nപ്രപഞ്ചത്തിലെങ്ങും നിൻ ശക്തി വെളിപ്പെടുന്നു.",
                "en": "O Lord my God! When I in awesome wonder\nConsider all the works Thy hand hath made,\nI see the stars, I hear the rolling thunder,\nThy pow'r throughout the universe displayed:"
            },
            {
                "label": "Stanza 2 / ചരണം 2",
                "tag": "S2",
                "ml": "ദൈവം തൻ പുത്രനെ ഒഴിവാക്കാതെ,\nമരിക്കുവാൻ അയച്ചു എന്ന് ഞാൻ ചിന്തിക്കുമ്പോൾ,\nക്രൂശിൽ അവൻ സന്തോഷത്തോടെ എന്റെ ഭാരം വഹിച്ചു,\nഎന്റെ പാപം നീക്കുവാൻ രക്തം ചിന്തി മരിച്ചു.",
                "en": "And when I think that God, His Son not sparing,\nSent Him to die, I scarce can take it in;\nThat on the cross, my burden gladly bearing,\nHe bled and died to take away my sin:"
            },
            {
                "label": "Stanza 3 / ചരണം 3",
                "tag": "S3",
                "ml": "ക്രിസ്തു ആർപ്പോടെ വീണ്ടും വരുമ്പോൾ,\nഎന്നെ വീട്ടിലേക്ക് കൊണ്ടുപോകുമ്പോൾ, എൻ ഹൃദയത്തിൽ എന്ത് സന്തോഷം!\nഅപ്പോൾ ഞാൻ താണു വണങ്ങി ആരാധിക്കും,\nഎന്റെ ദൈവമേ, നീ എത്ര വലിയവൻ എന്ന് ഘോഷിക്കും!",
                "en": "When Christ shall come with shout of acclamation\nAnd take me home, what joy shall fill my heart!\nThen I shall bow in humble adoration,\nAnd there proclaim, my God, how great Thou art!"
            }
        ]
    },
    {
        "id": 33,
        "number": 33,
        "category": "English Hymns",
        "book": "Hymns of Faith",
        "title_ml": "യേശുവിലുണ്ടൊരു നല്ല സ്നേഹിതൻ (What a Friend We Have in Jesus)",
        "title_en": "What a Friend We Have in Jesus",
        "stanzas": [
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "യേശുവിൽ എത്രയോ നല്ല സ്നേഹിതനുണ്ട്,\nനമ്മുടെ പാപങ്ങളും ദുഃഖങ്ങളും വഹിക്കുവാൻ!\nഎല്ലാം പ്രാർത്ഥനയിൽ ദൈവത്തിന്റെ അടുക്കൽ\nകൊണ്ടുവരുവാൻ എത്ര വലിയ ഭാഗ്യം!",
                "en": "What a friend we have in Jesus,\nAll our sins and griefs to bear!\nWhat a privilege to carry\nEverything to God in prayer!"
            },
            {
                "label": "Stanza 2 / ചരണം 2",
                "tag": "S2",
                "ml": "നമുക്ക് എത്രയോ പ്രാവശ്യം സമാധാനം നഷ്ടപ്പെടുന്നു,\nഎത്രയോ വേദനകൾ നാം വെറുതെ സഹിക്കുന്നു,\nകാരണം എല്ലാം നാം പ്രാർത്ഥനയിൽ\nദൈവത്തിന്റെ അടുക്കൽ സമർപ്പിക്കുന്നില്ല!",
                "en": "Oh, what peace we often forfeit,\nOh, what needless pain we bear,\nAll because we do not carry\nEverything to God in prayer!"
            },
            {
                "label": "Stanza 3 / ചരണം 3",
                "tag": "S3",
                "ml": "നമുക്ക് പരീക്ഷണങ്ങളും പ്രലോഭനങ്ങളുമുണ്ടോ?\nഎവിടെയെങ്കിലും കഷ്ടതകളുണ്ടോ?\nനാം ഒരിക്കലും നിരാശപ്പെടരുത്;\nപ്രാർത്ഥനയിൽ കർത്താവിങ്കൽ കൊണ്ടുപോവുക!",
                "en": "Have we trials and temptations?\nIs there trouble anywhere?\nWe should never be discouraged;\nTake it to the Lord in prayer!"
            }
        ]
    },
    {
        "id": 34,
        "number": 34,
        "category": "English Hymns",
        "book": "Hymns of Faith",
        "title_ml": "യേശു എന്റേതല്ലോ (Blessed Assurance)",
        "title_en": "Blessed Assurance, Jesus is Mine",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "ഇതാണ് എൻ ചരിത്രം, ഇതാണ് എൻ ഗാനം,\nഎൻ രക്ഷകനെ റോജും വാഴ്ത്തുന്നു ഞാൻ;\nഇതാണ് എൻ ചരിത്രം, ഇതാണ് എൻ ഗാനം,\nഎൻ രക്ഷകനെ റോജും വാഴ്ത്തുന്നു ഞാൻ!",
                "en": "This is my story, this is my song,\nPraising my Saviour all the day long;\nThis is my story, this is my song,\nPraising my Saviour all the day long!"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "ധന്യമാം ഉറപ്പ്, യേശു എന്റേതാണ്!\nദിവ്യ മഹത്വത്തിന്റെ ഒരു മുന്നാസ്വാദനം!\nരക്ഷയുടെ അവകാശി, ദൈവത്താൽ വിലയ്ക്കെടുക്കപ്പെട്ടവൻ,\nആത്മാവിനാൽ ജനിച്ചവൻ, രക്തത്താൽ കഴുകപ്പെട്ടവൻ.",
                "en": "Blessed assurance, Jesus is mine!\nOh, what a foretaste of glory divine!\nHeir of salvation, purchase of God,\nBorn of His Spirit, washed in His blood."
            },
            {
                "label": "Stanza 2 / ചരണം 2",
                "tag": "S2",
                "ml": "പൂർണ്ണ സമർപ്പണം, തികഞ്ഞ ആനന്ദം,\nമഹത്വ ദർശനങ്ങൾ ഇപ്പോൾ എൻ കൺമുമ്പിൽ വിരിയുന്നു;\nസ്വർഗ്ഗത്തിൽ നിന്നുള്ള ദൂതന്മാർ താഴേക്ക് കൊണ്ടുവരുന്നു\nകരുണയുടെ പ്രതിധ്വനികളും സ്നേഹത്തിന്റെ മന്ത്രങ്ങളും.",
                "en": "Perfect submission, perfect delight,\nVisions of rapture now burst on my sight;\nAngels descending, bring from above\nEchoes of mercy, whispers of love."
            }
        ]
    },
    {
        "id": 35,
        "number": 35,
        "category": "English Hymns",
        "book": "Hymns of Faith",
        "title_ml": "നിൻ വിശ്വസ്തത എത്രയോ വലിയത് (Great is Thy Faithfulness)",
        "title_en": "Great is Thy Faithfulness",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "നിൻ വിശ്വസ്തത എത്രയോ വലിയത്!\nപ്രഭാതം തോറും പുതിയ കൃപകൾ ഞാൻ കാണുന്നു;\nഎനിക്ക് ആവശ്യമുള്ളതെല്ലാം നിൻ കരം നൽകിയിരിക്കുന്നു;\nനിൻ വിശ്വസ്തത എത്രയോ വലിയത്, കർത്താവേ എനിക്ക്!",
                "en": "Great is Thy faithfulness! Great is Thy faithfulness!\nMorning by morning new mercies I see;\nAll I have needed Thy hand hath provided;\nGreat is Thy faithfulness, Lord, unto me!"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "നിൻ വിശ്വസ്തത എത്രയോ വലിയത്, പിതാവാം ദൈവമേ,\nനിന്നിൽ തിരിയുന്നതിന്റെ യാതൊരു നിഴലുമില്ല;\nനീ ഒരിക്കലും മാറുന്നില്ല, നിൻ അനുകമ്പ പരാജയപ്പെടുന്നില്ല;\nനീ എന്നേക്കും നിലകൊള്ളുന്നതുപോലെ തന്നെ തുടരും.",
                "en": "Great is Thy faithfulness, O God my Father,\nThere is no shadow of turning with Thee;\nThou changest not, Thy compassions, they fail not;\nAs Thou hast been Thou forever wilt be."
            },
            {
                "label": "Stanza 2 / ചരണം 2",
                "tag": "S2",
                "ml": "പാപമോചനം, നിലനിൽക്കുന്ന സമാധാനം,\nനയിക്കുവാനുള്ള നിന്റെ സാന്നിധ്യം;\nഇന്നത്തെ ശക്തിയും നാളത്തെ പ്രകാശമാനമായ പ്രത്യാശയും,\nഎണ്ണമറ്റ അനുഗ്രഹങ്ങളും എനിക്കായി നീ ഒരുക്കിയിരിക്കുന്നു!",
                "en": "Pardon for sin and a peace that endureth,\nThine own dear presence to cheer and to guide;\nStrength for today and bright hope for tomorrow,\nBlessings all mine, with ten thousand beside!"
            }
        ]
    },
    {
        "id": 36,
        "number": 36,
        "category": "English Hymns",
        "book": "Hymns of Faith",
        "title_ml": "ക്രിസ്തുവിൽ മാത്രം (In Christ Alone)",
        "title_en": "In Christ Alone",
        "stanzas": [
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "ക്രിസ്തുവിൽ മാത്രം എന്റെ പ്രത്യാശ അധിഷ്ഠിതമാണ്;\nഅവനാണ് എന്റെ വെളിച്ചം, എന്റെ ശക്തി, എന്റെ ഗാനം;\nഈ മൂലക്കല്ല്, ഈ ഉറപ്പുള്ള പാറക്കല്ല്,\nകഠിനമായ വരൾച്ചയിലും കൊടുങ്കാറ്റിലും ഉറച്ചുനിൽക്കുന്നു.",
                "en": "In Christ alone my hope is found,\nHe is my light, my strength, my song;\nThis Cornerstone, this solid Ground,\nFirm through the fiercest drought and storm."
            },
            {
                "label": "Stanza 2 / ചരണം 2",
                "tag": "S2",
                "ml": "ക്രൂശിൽ യേശു മരിച്ചപ്പോൾ,\nദൈവത്തിന്റെ നീതി പൂർണ്ണമായി തൃപ്തിപ്പെട്ടു;\nഎല്ലാ പാപങ്ങളും അവന്റെ മേൽ ചുമത്തപ്പെട്ടു;\nക്രിസ്തുവിന്റെ മരണത്തിൽ ഞാൻ ജീവിക്കുന്നു.",
                "en": "There on the cross as Jesus died,\nThe wrath of God was satisfied;\nFor every sin on Him was laid;\nHere in the death of Christ I live."
            },
            {
                "label": "Stanza 3 / ചരണം 3",
                "tag": "S3",
                "ml": "പാതാളത്തിൽ അവന്റെ ശരീരം കിടന്നു,\nലോകത്തിന്റെ വെളിച്ചം അന്ധകാരത്തിൽ കൊല്ലപ്പെട്ടു;\nപിന്നെ ആ മഹത്തായ ദിനത്തിൽ അവൻ ഉയിർത്തെഴുന്നേറ്റു,\nമരണത്തിന്റെ ശക്തിയെ തകർത്തു കളഞ്ഞു!",
                "en": "There in the ground His body lay,\nLight of the world by darkness slain;\nThen bursting forth in glorious day,\nUp from the grave He rose again!"
            },
            {
                "label": "Stanza 4 / ചരണം 4",
                "tag": "S4",
                "ml": "പാപത്തിന്റെ ഭയമില്ല, മരണത്തിന്റെ ഭയമില്ല,\nഇതാണ് എന്നിലെ ക്രിസ്തുവിന്റെ ശക്തി;\nആദ്യ ശ്വാസം മുതൽ അന്ത്യ ശ്വാസം വരെ,\nയേശു എന്റെ ജീവിതത്തെ നയിക്കുന്നു.",
                "en": "No guilt in life, no fear in death,\nThis is the power of Christ in me;\nFrom life's first cry to final breath,\nJesus commands my destiny."
            }
        ]
    },
    {
        "id": 37,
        "number": 37,
        "category": "English Hymns",
        "book": "Hymns of Faith",
        "title_ml": "പരിശുദ്ധൻ! പരിശുദ്ധൻ! പരിശുദ്ധൻ! (Holy, Holy, Holy)",
        "title_en": "Holy, Holy, Holy! Lord God Almighty",
        "stanzas": [
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "പരിശുദ്ധൻ, പരിശുദ്ധൻ, പരിശുദ്ധൻ! സർവ്വശക്തനായ ദൈവമേ!\nഉഷസ്സിൽ ഞങ്ങളുടെ ഗാനം നിന്നിലേക്ക് ഉയരും;\nപരിശുദ്ധൻ, പരിശുദ്ധൻ, പരിശുദ്ധൻ! കരുണാമയനും സർവ്വശക്തനുമായവനേ!\nത്രിയേക ദൈവമേ, വാഴ്ത്തപ്പെട്ട ത്രിത്വമേ!",
                "en": "Holy, Holy, Holy! Lord God Almighty!\nEarly in the morning our song shall rise to Thee;\nHoly, Holy, Holy! Merciful and Mighty!\nGod in three Persons, blessed Trinity!"
            },
            {
                "label": "Stanza 2 / ചരണം 2",
                "tag": "S2",
                "ml": "പരിശുദ്ധൻ, പരിശുദ്ധൻ, പരിശുദ്ധൻ! അന്ധകാരം നിന്നെ മറച്ചാലും,\nപാപിയുടെ കണ്ണ് നിന്റെ മഹത്വം കാണുന്നില്ലെങ്കിലും,\nനീ മാത്രം പരിശുദ്ധനാണ്; നിന്നെയല്ലാതെ വേറൊരുവനുമില്ല,\nശക്തിയിലും സ്നേഹത്തിലും വിശുദ്ധിയിലും തികഞ്ഞവനേ!",
                "en": "Holy, Holy, Holy! Though the darkness hide Thee,\nThough the eye of sinful man Thy glory may not see,\nOnly Thou art holy; there is none beside Thee,\nPerfect in power, in love, and purity."
            }
        ]
    },
    {
        "id": 38,
        "number": 38,
        "category": "English Hymns",
        "book": "Hymns of Faith",
        "title_ml": "ദൈവത്തിന്നു മഹത്വം (To God Be the Glory)",
        "title_en": "To God Be the Glory",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "കർത്താവിനെ സ്തുതിപ്പിൻ, ഭൂമി അവൻ ശബ്ദം കേൾക്കട്ടെ!\nകർത്താവിനെ സ്തുതിപ്പിൻ, ജനങ്ങൾ സന്തോഷിക്കട്ടെ!\nപിതാവിന്റെ അടുക്കൽ യേശുപുത്രനിലൂടെ വരിക,\nഅവൻ ചെയ്ത വലിയ കാര്യങ്ങൾക്കായി അവനു മഹത്വം നൽകുക!",
                "en": "Praise the Lord, praise the Lord, let the earth hear His voice!\nPraise the Lord, praise the Lord, let the people rejoice!\nO come to the Father, through Jesus the Son,\nAnd give Him the glory, great things He hath done!"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "ദൈവത്തിന് മഹത്വം, അവൻ മഹത്തായ കാര്യങ്ങൾ ചെയ്തിരിക്കുന്നു;\nഅവൻ ലോകത്തെ സ്നേഹിച്ചു തന്റെ പുത്രനെ നൽകി,\nനമ്മുടെ പാപങ്ങൾക്ക് പരിഹാരമായി ജീവൻ ത്യാഗം ചെയ്തു,\nജീവനിലേക്കുള്ള വാതിൽ എല്ലാവർക്കുമായി തുറന്നു തന്നു.",
                "en": "To God be the glory, great things He hath done;\nSo loved He the world that He gave us His Son,\nWho yielded His life an atonement for sin,\nAnd opened the life-gate that all may go in."
            }
        ]
    },
    {
        "id": 39,
        "number": 39,
        "category": "English Hymns",
        "book": "Hymns of Faith",
        "title_ml": "എന്നെ കടന്നുപോകരുതേ (Pass Me Not, O Gentle Savior)",
        "title_en": "Pass Me Not, O Gentle Savior",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "രക്ഷകാ, രക്ഷകാ, എന്റെ പ്രാർത്ഥന കേൾക്കേണമേ;\nമറ്റുള്ളവരെ നീ വിളിക്കുമ്പോൾ,\nഎന്നെ കടന്നുപോകരുതേ!",
                "en": "Savior, Savior, hear my humble cry;\nWhile on others Thou art calling,\nDo not pass me by!"
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "ശാന്തനായ രക്ഷകാ, എന്നെ കടന്നുപോകരുതേ;\nഎന്റെ താഴ്മയുള്ള നിലവിളി കേൾക്കേണമേ;\nമറ്റുള്ളവരെ നീ വിളിക്കുമ്പോൾ,\nഎന്നെ കടന്നുപോകരുതേ!",
                "en": "Pass me not, O gentle Savior,\nHear my humble cry;\nWhile on others Thou art calling,\nDo not pass me by."
            }
        ]
    },
    {
        "id": 40,
        "number": 40,
        "category": "English Hymns",
        "book": "Hymns of Faith",
        "title_ml": "യേശുവിലേക്ക് കണ്ണുകൾ തിരിക്കുക (Turn Your Eyes Upon Jesus)",
        "title_en": "Turn Your Eyes Upon Jesus",
        "stanzas": [
            {
                "label": "Chorus / പല്ലവി",
                "tag": "C",
                "ml": "നിന്റെ കണ്ണുകളെ യേശുവിലേക്ക് തിരിക്കുക,\nഅവന്റെ അത്ഭുത മുഖത്തേക്ക് നോക്കുക,\nഅപ്പോൾ അവന്റെ മഹത്വത്തിന്റെയും കൃപയുടെയും വെളിച്ചത്തിൽ\nഭൂമിയിലെ കാര്യങ്ങൾ വിചിത്രമായി മങ്ങിപ്പോകും.",
                "en": "Turn your eyes upon Jesus,\nLook full in His wonderful face,\nAnd the things of earth will grow strangely dim,\nIn the light of His glory and grace."
            },
            {
                "label": "Stanza 1 / ചരണം 1",
                "tag": "S1",
                "ml": "ക്ഷീണിച്ച ആത്മാവേ, നീ ഇരുട്ടിൽ നടക്കുകയാണോ?\nനിന്റെ കണ്ണുകൾ കണ്ണീരണിഞ്ഞിരിക്കുന്നുവോ?\nരക്ഷകന്റെ സന്നിധിയിൽ ജീവന്റെ വെളിച്ചമുണ്ട്,\nനിത്യ പ്രകാശം നിന്നിൽ നിറയട്ടെ!",
                "en": "O soul, are you weary and troubled?\nNo light in the darkness you see?\nThere’s light for a look at the Savior,\nAnd life more abundant and free!"
            }
        ]
    }
]

out_path = os.path.join(os.path.dirname(__file__), 'songs_database.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(songs, f, ensure_ascii=False, indent=2)

print(f"Successfully generated songs_database.json with {len(songs)} authentic Malayalam & English hymns at {out_path}!")

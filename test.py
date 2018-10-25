from emotion import Extractor

article = [u"""The Bharatiya Janata Party (BJP) on Wednesday demanded from Delhi Chief Minister Arvind Kejriwal to remove Cabinet Minister Kailash Gahlot from his post. Earlier in the day, Income Tax sleuths carried out searches at 16 residential and business premises linked to Gahlot and his family members in the national capital and Gurugram.
"Kejriwal should immediately remove Gahlot as Transport Minister in view of the Income Tax raids at his 16 premises in connection with business operated and owned by his family," leader of Opposition in Delhi Assembly and BJP leader Vijender Gupta said in a statement here.
"Today, another gem of Kejriwal's 67 gems got exposed," he said adding that the Income Tax Department was not allowed to work in an independent and fair manner. 
Meanwhile, Kejriwal asked Prime Minister Narendra Modi to apologise for 'constantly troubling' the Aam Aadmi Party (AAP) government after the Income Tax Department carried out raids.
Kejriwal accused the Modi government of trying to 'intimidate' the AAP dispensation by getting its leaders and ministers raided by central agencies.
The party also termed the raid as 'political vendetta'.
"Friendship with Nirav Modi and Mallya and raid on us? Modiji you conducted raids on me Satyendar and Manish what happened to those (raids). Nothing was found. So before you go with another raid at least apologise to Delhi people for troubling their elected government," Kejriwal tweeted.""",
           u"""West Bengal chief minister and Trinamool Congress (TMC) chief Mamata Banerjee's efforts to rename the state as 'Bangla' have again faced an obstacle from the Ministry of Home Affairs (MHA).
According to The Indian Express, the home ministry has expressed concern over this move, saying that the name "may sound like Bangladesh and that it would be difficult to differentiate the two at international forums". The home ministry has written to the Ministry of External Affairs, the report said, to obtain an opinion before any further consideration.
However, in 2016, Mamata had addressed the possibility of the name being confused with Bangladesh. Noting that the name 'Bangla' had historical significance, she had said, "In English it will be Bengal, so that there will be no confusion with the name of neighbouring Bangladesh."
A constitutional amendment is required for a change in the name of a state. A recent example of the name of a state being changed was that of Odisha (earlier called Orissa).
Banerjee's plans to rename the state have been taking shape since 2011, when the newly elected chief minister had put forward 'Paschim Banga' as an option.
Banerjee's effort in 2011 never saw the light of day at the Centre, and was unsuccessful even in 2016 when the state Assembly passed a resolution to change the name of West Bengal to language-specific names. The cabinet had proposed that the name of the state be 'Bengal' in English, 'Bangla' in Bengali, and 'Bangal' in Hindi. Then, the home ministry had rejected the proposal saying that it would not be possible for a state to have different names in different languages.
However, in July this year, the West Bengal Assembly unanimously passed a resolution to change the state's name to 'Bangla'.
According to reports, the state's Assembly pushed more strongly for the renaming after the July 2016 Inter-State Council meeting in Delhi, when Banerjee was the last chief minister to address the Council because the speakers were listed in alphabetical order of the states. The name 'Bangla' would bump the state up in an alphabetically-organised list to number four.
Apart from political repercussions of the move to rename the state, with the Left, Congress, and BJP state parties walking out of the Assembly in August 2016 over the issue, political analysts have warned against reigniting tensions in the Darjeeling and Kalimpong areas of the state. People residing in "the hills" as the areas are colloquially referred to, had in 2017 initiated a strong resistance to the state government's move to make Bengali a mandatory language in schools in the state.
The Gorkha and Nepali communities of the state demanded a separate state "Gorkhaland" in protest and as an assertion of the linguistic differences in the state. Even though those protests were successfully pacified by the Mamata Banerjee-government after three months, experts believe that there continues to be a divide in socio-cultural aspects in the state.
As this report by Marcus Dam points out, the attempt to rename the state may not go down well in the hills, as "Bangla" is also the locally accepted term for the Bengali language."""]

if __name__ == "__main__":
  for index, a in enumerate(article):
      news = Extractor(a)
      print('------------------------------------------ {} -----------------------------------------'.format(index))
      print("Cities : {} \n\nPoliticains : {} \n\nStates : {}\n".format(news.cities, news.politicains, news.states))
      print("Persons : {} \n\nOrganiztion : {}\n".format(news.persons, news.organization))
      print("Commons Words : {}\n".format(news.commonWords))
      print("Emotions Classification : {}\n\nEmotion Intensities : {}\n\nEmotion Intensities Category : {}".format(news.emotion_class, news.emotion_intensities,
            news.emotions_intensities_cat))
      print('----------------------------------------------------------------------------------------\n\n')
import tkinter as tk
from tkinter import scrolledtext
import random
import requests
from bs4 import BeautifulSoup
import string


class CharacterGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Anime Character & Prompt Generator")
        self.root.geometry("700x600")

        # UI Elements
        self.is_nsfw = tk.BooleanVar(value=False)
        
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(pady=10)

        self.nsfw_checkbox = tk.Checkbutton(
            self.top_frame, 
            text="NSFW Mode (Restricts age to 18-25 & adds tags)", 
            variable=self.is_nsfw,
            font=("Arial", 10, "bold")
        )
        self.nsfw_checkbox.pack(side=tk.LEFT, padx=10)

        self.generate_btn = tk.Button(
            self.top_frame, 
            text="Generate Character", 
            command=self.generate, 
            bg="#4CAF50", 
            fg="white", 
            font=("Arial", 12, "bold")
        )
        self.generate_btn.pack(side=tk.LEFT, padx=10)

        self.log_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 11))
        self.log_area.pack(expand=True, fill='both', padx=15, pady=15)

        # Attribute Data
        is_nsfw = self.is_nsfw.get()
        
        if is_nsfw:
               self.chest_sizes = ["flat chest", "near-flat chest", "tiny breasts", "small breasts", "medium breasts", "large breasts"]
        else:
               self.chest_sizes = ["flat chest", "near-flat chest", "tiny breasts", "small breasts"]
        
        self.base_colors = [
            "Ebony Black", "Ash Gray", "Silver Gray", "Ivory White", "Crimson Red", 
            "Chocolate Brown", "Bronze Brown", "Citrus Orange", "Golden Blonde", 
            "Kiwi Lime", "Emerald Green", "Seafoam Turquoise", "Sky Cyan", 
            "Azure Blue", "Dusk Violet", "Royal Purple", "Aromatic Lavender", 
            "Plum Magenta", "Strawberry Pink"
        ]
        
        self.names = [
            "Aagot", "Aarushi", "Abba", "Abby", "Abeer", "Abena", "Abida", "Abidemi", "Abigail", "Abiha", "Abijah", "Abike",
            "Abimbola", "Abiola", "Abisola", "Abla", "Abosede", "Abou", "Açelya", "Acey", "Ada", "Adalgisa", "Adama", "Adame",
            "Adaobi", "Addie", "Addison", "Adea", "Adebimpe", "Adebisi", "Adebola", "Adedoyin", "Adee", "Adejoke", "Adela",
            "Adelaide", "Adelasia", "Adele", "Adelheid", "Adelina", "Adeline", "Adena", "Aderonke", "Adila", "Adile", "Adina", "Aditi",
            "Adléta", "Adna", "Adora", "Adria", "Adriana", "Adriane", "Adrianne", "Adrienn", "Adrienne", "Adrijana", "Adunni", "Adut",
            "Adwoa", "Æbbe", "Aodhamair", "Ælfgifu", "Aella", "Aemilia", "Aenor", "Aerin", "Aet", "Æthelburh", "Afaf", "Afag", "Aferdita",
            "Afra", "Afreen", "África", "Afroditi", "Afsana", "Afua", "Agafa", "Agafiya", "Agafokliya", "Agafya", "Agapa", "Agapiya",
            "Agariste", "Agata", "Agatha", "Agathe", "Agboola", "Ageeth", "Ageha", "Aglaé", "Agnė", "Agnes", "Agnese", "Agneta",
            "Agnieszka", "Agrippina", "Agustina", "Ahad", "Ahhotep", "Ahlam", "Ahna", "Ai", "Aibhilín", "Aoibheann", "Aida", "Aifric",
            "Aiga", "Aigul", "Aigul", "Aija", "Aika", "Aiko", "Aila", "Aileen", "Aili", "Ailsa", "Aime", "Aimée", "Aimi", "Aimie", "Aina",
            "Ainara", "Áine", "Aino", "Ainslie", "Aira", "Aire", "Airi", "Aisha", "Aishwarya", "Aisling", "Aistė", "Aitana", "Ajda", "Ajla",
            "Ajoke", "Akane", "Akari", "Akemi", "Akeno", "Akgül", "Akhila", "Aki", "Akie", "Akiko", "Akina", "Akino", "Akiyo", "Ako",
            "Akosua", "Akoya", "Akua", "Akvilė", "Aladi", "Alafair", "Alaide", "Alaina", "Alanah", "Alanna", "Alannah", "Alanoud", "Alara",
            "Alazne", "Alba", "Albane", "Alberta", "Albertina", "Albertine", "Albina", "Albinia", "Albulena", "Alcira", "Alda", "Aldea",
            "Aldona", "Aleana", "Aleena", "Aleida", "Alejandra", "Alena", "Alene", "Alenka", "Alessa", "Alessandra", "Alessia", "Alethaire",
            "Alethea", "Aletta", "Alette", "Alev", "Alevtina", "Alex", "Alexa", "Alexandra", "Alexandria", "Alexia", "Alexina", "Alexis",
            "Aleyna", "Alfhild", "Alfonsina", "Alia", "Alice", "Alicia", "Alida", "Alide", "Aliette", "Aliki", "Alima", "Alina", "Aline", "Alisa",
            "Alisha", "Alison", "Aliya", "Aliyah", "Aliye", "Aliza", "Alizé", "Alla", "Allegra", "Allene", "Alli", "Allira", "Ally", "Allyson", "Alma",
            "Almila", "Almudena", "Almut", "Almuth", "Aloma", "Alona", "Alondra", "Alora", "Alruna", "Alta", "Altagracia", "Altan", "Althea",
            "Altinay", "Altynai", "Alvina", "Alvira", "Alya", "Alyce", "Alycia", "Alyona", "Alys", "Alyson", "Alyssa", "Ama", "Amabel", "Amalia",
            "Amalie", "Amanda", "Amandine", "Amane", "Amaryllis", "Amat", "Amaya", "Amber", "Amberley", "Ambika", "Ambre", "Amelia",
            "Amélie", "Amethyst", "Ami", "Amicie", "Amina", "Aminata", "Amira", "Amisha", "Amita", "Amity", "Amna", "Amparo", "Amrita",
            "Amy", "Ana", "Ana Lilia", "Anabel", "Anabelle", "Anahit", "Anahita", "Anaida", "Anaïs", "Analyn", "Anamaria", "Anamarija", "Anan",
            "Ananya", "Anastacia", "Anastase", "Anastasia", "Anastasie", "Anastasiia", "Anastasija", "Anastasiya", "Anastassia", "Anastassiya",
            "Anasuya", "Anat", "Anaya", "Anca", "Ancuța", "Anda", "Anđela", "Anđelka", "Andra", "Andrada", "Andrea", "Andréanne", "Andrée",
            "Andreea", "Andréia", "Andreina", "Andreja", "Andrijana", "Andy", "Aneta", "Anete", "Anett", "Anette", "Angel", "Angela", "Angèle",
            "Angelica", "Angelika", "Angeliki", "Angelina", "Angélique", "Angella", "Angharad", "Angie", "Ani", "Anica", "Anicka", "Aniela",
            "Anika", "Anikó", "Anila", "Anisa", "Anisha", "Anissa", "Anita", "Anitra", "Anjali", "Anju", "Anka", "Ankhesenpepi", "Ankica", "Ankita",
            "Ann", "Anna", "Annabella", "Annabelle", "Annabeth", "Annalena", "Annalisa", "Annamari", "Annamaria", "Annastacia", "Annastasia",
            "Anne", "Annegret", "Anneke", "Anneli", "Annelie", "Annelies", "Anneliese", "Annely", "Annemarie", "Annemieke", "Annett", "Annetta",
            "Annette", "Anni", "Annice", "Annie", "Annika", "Anniken", "Annina", "Annita", "Annot", "Annunziata", "Anoma", "Anouk", "Anoushka",
            "Ans", "Anthea", "Anthonia", "Anthonie", "Antionette", "Antje", "Antoinette", "Antonela", "Antonella", "Antonia", "Antonie", "Antonieta",
            "Antonietta", "Antonija", "Antonina", "Antonine", "Antoniya", "Anu", "Anula", "Anupama", "Anuradha", "Anushree", "Anwen", "Anya",
            "Anzu", "Aoife", "Aori", "Aparna", "Apoorva", "April", "Arabella", "Araceli", "Aranka", "Arantxa", "Araz", "Arda", "Ardeth", "Ardis",
            "Areej", "Arete", "Aretha", "Arevik", "Ari", "Aria", "Ariadna", "Ariadne", "Ariana", "Ariel", "Ariella", "Arielle", "Ariko", "Arina", "Arisa",
            "Arja", "Arjola", "Arkadyevna", "Arleen", "Arlette", "Arline", "Arminda", "Armita", "Arndís", "Arnhild", "Arpine", "Arpita", "Arta", "Arti",
            "Arundhati", "Arusyak", "Arwa", "Arya", "Arzu", "Åsa", "Asa", "Asaka", "Asako", "Asami", "Asana", "Asano", "Ásdís", "Asena", "Ash",
            "Åshild", "Ashleigh", "Ashley", "Ashlyn", "Ashraqat", "Asja", "Aslaug", "Asli", "Aslihan", "Asma", "Aspen", "Assunta", "Asta", "Aster",
            "Astou", "Astra", "Astrid", "Asu", "Asude", "Asuman", "Asumi", "Asuna", "Asya", "Atarah", "Atefeh", "Athena", "Athenais", "Athira",
            "Atikah", "Atinuke", "Atsede", "Atsuko", "Atsumi", "Attia", "Aubrey", "Aud", "Aude", "Audra", "Audrey", "Auður", "Auguste", "Augustina",
            "Augustine", "Auksė", "Aulikki", "Aurea", "Aurelia", "Aurélie", "Aurora", "Aurore", "Ausma", "Aušra", "Aušrinė", "Austra", "Autumn", "Ava",
            "Avdotya", "Ave", "Avelina", "Avenira", "Aventina", "Averil", "Avgusta", "Avgustina", "Aviafa", "Aviana", "Avice", "Avie", "Avigail", "Avis",
            "Avital", "Aviva", "Avlida", "Avreliya", "Avreya", "Avtonoma", "Axelle", "Aya", "Ayaka", "Ayako", "Ayala", "Ayame", "Ayami", "Ayana",
            "Ayane", "Ayanna", "Ayano", "Ayasa", "Aybike", "Aybüke", "Ayça", "Aycan", "Ayda", "Aydan", "Ayfer", "Aygerim", "Aygül", "Ayla", "Aylin",
            "Aynur", "Ayoka", "Ayşegül", "Aysel", "Ayşenur", "Aysu", "Ayten", "Ayu", "Ayuka", "Ayuko", "Ayumi", "Ayumu", "Ayuru", "Azadeh", "Azalea",
            "Azita", "Azize", "Azra", "Azucena", "Azumi", "Azura", "Azza", "Azzurra", "Babette", "Badia", "Badr", "Bahar", "Bahia", "Baiba", "Bailey",
            "Bailie", "Balqis", "Bandari", "Banu", "Bara", "Baran", "Barb", "Barbara", "Bärbel", "Barbora", "Barbro", "Barrdhubh", "Başak", "Basia", "Basilia",
            "Basilica", "Basma", "Bathsheba", "Bathsheba", "Batsheva", "Battsetseg", "Bayley", "Bé Fáil", "Bea", "Bean", "Beata", "Béatrice", "Beatrice",
            "Beatrix", "Beatriz", "Beau", "Béḃinn", "Becca", "Becki", "Becky", "Bediha", "Begoña", "Begum", "Behice", "Běla", "Belen", "Belgin", "Belinda",
            "Belkis", "Bella", "Belle", "Ben Muman", "Benazir", "Benedicta", "Bénédicte", "Bengi", "Bengisu", "Bengü", "Beni", "Benjamina", "Benvenida",
            "Beren", "Berengaria", "Bérengère", "Berenice", "Berfin", "Berfu", "Bergljot", "Beril", "Berna", "Bernadeta", "Bernadett", "Bernadetta",
            "Bernadette", "Bernadine", "Bernette", "Berrak", "Berrin", "Berta", "Bertha", "Bertina", "Beryl", "Bess", "Bessie", "Beth", "Bethan", "Bethany",
            "Betje", "Betsabé", "Betsy", "Bettany", "Bette", "Bettina", "Betty", "Bettye", "Betül", "Beulah", "Beverly", "Beyza", "Bianca", "Bianka",
            "Bibian", "Bibiane", "Bice", "Bienvenida", "Bijal", "Bike", "Biljana", "Bilkisu", "Bilyana", "Binita", "Binny", "Bintou", "Bipasha", "Birgit",
            "Birgithe", "Birgitta", "Birgitte", "Birgül", "Birsen", "Birte", "Birthe", "Biruta", "Bisa", "Bisera", "Bisola", "Bita", "Bitsy", "Bitte", "Björg",
            "Bjørk", "Björk", "Blair", "Blake", "Blanca", "Blanche", "Blanchefleur", "Blandine", "Blanka", "Blenda", "Blerta", "Blodwen", "Blossom",
            "Blythe", "Bobbi", "Bobby", "Bodil", "Boel", "Boglárka", "Bogna", "Bogumiła", "Bohumila", "Bojana", "Bolade", "Bolette", "Bonita", "Bonnie",
            "Bonny", "Borghild", "Borislava", "Borka", "Boutheina", "Boyanka", "Božena", "Bożena", "Braden", "Brandi", "Brandy", "Branislava", "Branka",
            "Brankica", "Branwen", "Branwen", "Bratislava", "Breanna", "Breanne", "Bree", "Brenda", "Brett", "Bria", "Brianda", "Brianna", "Brianne",
            "Brianne", "Bridget", "Bridgetta", "Bridgette", "Brielle", "Briget", "Brigid", "Brigita", "Brigitte", "Brilliana", "Brina", "Brita", "Britnee", "Britt",
            "Britta", "Brittany", "Brittny", "Brodie", "Bronislava", "Bronisława", "Bronwen", "Bronwyn", "Brooklyn", "Brooks", "Brunhilde", "Bryn", "Bryna",
            "Brynhild", "Brynhildur", "Brynlee", "Bryony", "Buddug", "Buffy", "Büke", "Burçak", "Burçin", "Burcu", "Burdine", "Burgl", "Buse", "Bushra",
            "Busisiwe", "Cacht", "Caden", "Cadence", "Cady", "Çağla", "Cainnech", "Cairine", "Cairistìona", "Caitlin", "Caitlín", "Caitríona", "Caitrìona",
            "Caley", "Calixte", "Calla", "Callie", "Callista", "Callisto", "Callisto", "Cally", "Camelia", "Camilla", "Camille", "Camryn", "Canan", "Candace",
            "Candan", "Candice", "Candida", "Candy", "Cansel", "Cansever", "Cansu", "Caoilainn", "Caoilfhionn", "Caoimhe", "Cara", "Caralee", "Cari",
            "Cariad", "Carin", "Carina", "Carine", "Caris", "Carissa", "Carità", "Carla", "Carlee", "Carleigh", "Carlena", "Carlene", "Carlette", "Carlie",
            "Carlijn", "Carlina", "Carline", "Carlota", "Carlota", "Carlotta", "Carly", "Carlyn", "Carman", "Carmelina", "Carmelita", "Carmen", "Carol",
            "Carola", "Carole", "Carolee", "Carolien", "Carolijn", "Carolina", "Caroline", "Carolyn", "Carolyne", "Carolynne", "Carrie", "Carroll", "Carry",
            "Carson", "Cary", "Carys", "Casey", "Cassandra", "Cassidy", "Cataleya", "Cătălina", "Catalina", "Cătălina", "Catarina", "Caterina", "Cath",
            "Catharina", "Catharine", "Catherina", "Cathie", "Cathleen", "Cathy", "Catiuscia", "Catriona", "Catríona", "Catrìona", "Cayetana", "Caylee",
            "Cecelie", "Cecil", "Cécile", "Cecilia", "Cecilie", "Cecily", "Celeste", "Celestia", "Celestina", "Celia", "Celinda", "Céline", "Cemre", "Ceren",
            "Ceridwen", "Cerys", "Ceyda", "Ceylan", "Chaima", "Chalita", "Chamikara", "Chandrani", "Chandrika", "Chanelle", "Chantae", "Chantal",
            "Chantelle", "Chapa", "Char", "Chara", "Charikleia", "Charis", "Charisse", "Charitina", "Charity", "Charla", "Charle", "Charlee", "Charlene",
            "Charley", "Charli", "Charlie", "Charline", "Charlize", "Charlot", "Charlotta", "Charlotte", "Charly", "Charlyne", "Charmaine", "Charmian",
            "Charna", "Charné", "Chas", "Chasity", "Chastity", "Chaya", "Chelsea", "Cheri", "Cherilyn", "Cherine", "Cherry", "Cheryl", "Cheska", "Chetna",
            "Chiara", "Chidinma", "Chidori", "Chie", "Chieko", "Chiemi", "Chieno", "Chigusa", "Chihana", "Chiharu", "Chihaya", "Chiho", "Chika", "Chikage",
            "Chikako", "Chinami", "Chinatsu", "Chinenye", "Chioma", "Chisako", "Chisato", "Chise", "Chitose", "Chiya", "Chiyako", "Chiyo", "Chiyoko",
            "Chiyono", "Chiyori", "Chiyu", "Chizuko", "Chizuru", "Chloe", "Choko", "Chris", "Chrissie", "Chrissy", "Christa", "Christabel", "Christabel",
            "Christal", "Christelle", "Christene", "Christi", "Christiana", "Christiane", "Christina", "Christine", "Christophine", "Christy", "Chrystine",
            "Chunxia", "Ciara", "Çiğdem", "Cilla", "Cinderella", "Cindy", "Claire", "Clara", "Clare", "Claribel", "Clarice", "Clarinda", "Clarine", "Clarissa",
            "Claude", "Claudette", "Claudia", "Claudine", "Clelia", "Clemence", "Clémence", "Clemencia", "Clementia", "Clementina", "Clementine",
            "Clémentine", "Cleo", "Cleopatra", "Clio", "Clodagh", "Clorinda", "Clover", "Clytie", "Cobhlaith", "Cobie", "Cody", "Colette", "Colla", "Colleen",
            "Concepción", "Concetta", "Concha", "Conchita", "Constance", "Constanța", "Constanze", "Consuelo", "Cor", "Cora", "Coral", "Coralee",
            "Coralia", "Coralie", "Coraline", "Cordelia", "Corin", "Corina", "Corinna", "Corinne", "Corisande", "Cornelia", "Corrie", "Corrina", "Corryn",
            "Coryn", "Cosette", "Cosmina", "Costanza", "Courtney", "Cozi", "Crina", "Crino", "Crista", "Cristiana", "Cristina", "Cristine", "Cristy", "Croía",
            "Crystal", "Csilla", "Cunegundes", "Cushla", "Cybele", "Cynthia", "Cyra", "Dace", "Daenerys", "Dafna", "Dagmar", "Dagmara", "Dagny",
            "Dahlia", "Daiana", "Daiane", "Daiga", "Daila", "Daina", "Dainuvīte", "Daisy", "Dakota", "Dalal", "Dalene", "Dalia", "Dalida", "Dalilah", "Dallan",
            "Dalva", "Damayanti", "Damla", "Dana", "Danah", "Daneliya", "Danella", "Dani", "Danica", "Danie", "Daniela", "Daniele", "Danielle", "Daniëlle",
            "Danijela", "Danila", "Danka", "Danna", "Dannah", "Danguolė", "Danuta", "Danutė", "Daphna", "Daphne", "Darby", "Darcie", "Dareen", "Darerca",
            "Daria", "Dariga", "Darina", "Darla", "Darlene", "Darshika", "Davida", "Davina", "Davorka", "Dawn", "Dayana", "Dayna", "Dea", "Deandra",
            "DeAndrea", "Deanna", "Deanne", "Deb", "Debbie", "Deborah", "Debra", "Debrah", "Dede", "Deepa", "Deepali", "Deepika", "Deepti", "Defne",
            "Deianira", "Deidre", "Deimantė", "Deirdre", "Deirdre", "Deja", "Delaney", "Delena", "Delia", "Delilah", "Delphine", "Demet", "Demetria", "Demi",
            "Dena", "Denice", "Denisa", "Denise", "Denisse", "Denyce", "Denyse", "Derbforgaill", "Derin", "Dervla", "Désirée", "Desislava", "Despina",
            "Destiny", "Devon", "Diamond", "Diana", "Diane", "Dicle", "Didem", "Dijana", "Dilara", "Dilek", "Diletta", "Diljá", "Dilys", "Dimity", "Dina",
            "Dinara", "Dionne", "Dipuo", "Dita", "Ditte", "Dixie", "Diya", "Dobromila", "Dobromiła", "Dobromira", "Dobroniega", "Dobroslava", "Dobrosława",
            "Doğa", "Doina", "Doireann", "Dolores", "Dolors", "Domenica", "Dominga", "Dominika", "Dominique", "Domnina", "Donatella", "Donka", "Donna",
            "Donya", "Dóra", "Dora", "Dorah", "Dorcas", "Doreen", "Dorice", "Dorina", "Dorinda", "Doris", "Dorit", "Dorota", "Dorothea", "Dorothy", "Dorrie",
            "Dorries", "Dorrit", "Dorta", "Dorte", "Dot", "Dottie", "Doubravka", "Doutzen", "Dove", "Draga", "Dragana", "Dragica", "Draginja", "Drahomíra",
            "Drew", "Drita", "Drusilla", "Dub Lémna", "Dubh Essa", "Dubhchobhlaigh", "Duduzile", "Dulce", "Dulcie", "Dumitrița", "Dunja",
            "Dusa", "Duygu", "Dženita", "Dzidra", "Dzintra", "Eadgifu", "Ealdgyth", "Earlene", "Ebba", "Ebonee", "Eboni", "Ebony", "Ebru", "Ecaterina", "Ece",
            "Ecem", "Eda", "Edburga", "Edda", "Edel", "Edeltraud", "Edelweiss", "Eden", "Edie", "Edina", "Edit", "Edita", "Edith", "Édith", "Edna", "Edris",
            "Eduarda", "Edvarda", "Edwige", "Edwina", "Edyta", "Eefje", "Eeva", "Effie", "Eftychia", "Eglė", "Eha", "Ehala", "Eihi", "Eija", "Eiko", "Eila", "Eileen",
            "Eilidh", "Eilika", "Eilish", "Eimi", "Eirlys", "Eirwen", "Eithne", "Eivor", "Ekaterina", "Ekaterine", "Ekaterini", "Ela", "Elaine", "Elanor", "Elayne",
            "Elba", "Elçin", "Eldrid", "Elea", "Eleana", "Eleanor", "Eleanora", "Eleanora", "Electa", "Elektra", "Hajnalka", "Elen", "Elena", "Elene", "Eleni",
            "Eleonora", "Eleri", "Elfi", "Elfriede", "Eliana", "Éliane", "Elin", "Elina", "Elisa", "Elisabeta", "Elisabetta", "Elisapeta", "Élise", "Elisha", "Eliška",
            "Elissa", "Elita", "Elitsa", "Eliza", "Elizabeth", "Elizebeth", "Elke", "Ella", "Elle", "Ellen", "Ellesse", "Elli", "Ellie", "Ellis", "Elly", "Ellyse", "Elma",
            "Elmarie", "Elo", "Élodie", "Eloise", "Elora", "Els", "Elsa", "Else", "Elsebeth", "Elsie", "Elspeth", "Eluned", "Elva", "Elvira", "Elysia", "Elyssa", "Elza",
            "Elzbieta", "Ema", "Ember", "Embla", "Emel", "Emelia", "Emelie", "Emer", "Emerald", "Emi", "Emika", "Emiko", "Emilee", "Emilia",
            "Émilie", "Emily", "Emina", "Emine", "Emiri", "Emma", "Emmanuelle", "Emmeline", "Emmy", "Ena", "Endang", "Ene", "Eneli", "Enid", "Enikő", "Enni",
            "Enola", "Enora", "Enrica", "Epp", "Erena", "Erendiz", "Eri", "Ericka", "Erika", "Eriko", "Erin", "Erina", "Erline", "Ermengarde", "Ermentrude",
            "Ermentrude", "Ermina", "Erminia", "Erminie", "Ermyntrude", "Erna", "Ernestine", "Ersilia", "Erzsebet", "Eseosa", "Esfir", "Esih", "Eslanda", "Esma",
            "Esmeralda", "Esperanza", "Esra", "Essi", "Esta", "Estee", "Estefanía", "Estelita", "Estelle", "Ester", "Esther", "Esti", "Esty", "Eszter", "Eta", "Éadaoin",
            "Etelka", "Eteri", "Ethel", "Etheldreda", "Ethlyn", "Ethna", "Etsuko", "Etta", "Etty", "Eudine", "Eudora", "Eudora", "Eudoxia", "Eufemia", "Eugenia",
            "Eugénie", "Eugenija", "Euis", "Eula", "Eunice", "Euphemia", "Euphémie", "Eutychia", "Eva", "Evadne", "Evalena", "Evan", "Evangelia", "Evangelina",
            "Evangelista", "Evanthia", "Evdokija", "Evdokiya", "Ève", "Eve", "Evelia", "Evelin", "Evelina", "Evelyn", "Evelyne", "Evgenia", "Evi", "Evie", "Ewa",
            "Eylem", "Eylül", "Ezgi", "Fabia", "Fabienne", "Fabrizia", "Fadia", "Fadwa", "Fahda", "Faith", "Faiza", "Famke", "Fancy", "Fania", "Fannie", "Fanny",
            "Farah", "Farahnaz", "Fareeha", "Farhana", "Fariba", "Farida", "Fariza", "Farnaz", "Faryal", "Farzaneh", "Faten", "Fathia", "Fatima", "Fatuma",
            "Fausat", "Fausta", "Fawn", "Fawzia", "Fay", "Faye", "Fazila", "Fedelm", "Federica", "Felicia", "Félicie", "Felicita", "Felicity", "Femke", "Fen",
            "Fenella", "Fenny", "Fereshteh", "Ferial", "Feride", "Fern", "Fernanda", "Fernande", "Fethiye", "Ffion", "Fflu", "Fiadh", "Fiammetta", "Fidan",
            "Fidelia", "Fidelma", "Fides", "Fien", "Filipa", "Filippa", "Filiz", "Filomena", "Fíne", "Fíneamhain", "Finn", "Fiona", "Fionnghuala", "Fioralba",
            "Fiorella", "Fiorenza", "Fjolla", "Flaka", "Flann", "Flávia", "Flavia", "Fleur", "Fleurette", "Flicka", "Floortje", "Flora", "Florbela", "Flore", "Florence",
            "Florencia", "Florentina", "Florica", "Florina", "Florinda", "Florine", "Florrie", "Folake", "Folakemi", "Forbflaith", "Fortunata", "Fotini", "Fowzia",
            "Franca", "France", "Frances", "Francesca", "Franchesca", "Francie", "Francine", "Francisca", "Franciska", "Franciszka", "Françoise", "Frankie",
            "Franziska", "Frauke", "Frederica", "Frederique", "Freya", "Frida", "Friederike", "Friedl", "Fritzi", "Frøydis", "Fruzsina", "Fubuki", "Fujie", "Fujiko",
            "Fūka", "Fukumi", "Fumi", "Fumie", "Fumika", "Fumiko", "Fumino", "Funda", "Funmi", "Fusa", "Fusako", "Füsun", "Futaba", "Fuyuko", "Fuyumi",
            "Fyokla", "Gabbie", "Gabija", "Gabriela", "Gabriele", "Gabrielė", "Gabriella", "Gabrielle", "Gabrijela", "Gaetana", "Gaëtane", "Gage", "Gail", "Gaja",
            "Gala", "Gale", "Galina", "Galit", "Gamze", "Ganna", "Garance", "Garbiñe", "Gaudentia", "Gayane", "Gayatri", "Gayle", "Gaynor", "Gcina", "Geena",
            "Geerten", "Geertruida", "Gelsomina", "Gemma", "Gene", "Geneva", "Geneviève", "Genevieve", "Gennadiya", "Genovaitė", "Georgeana",
            "Georgeanna", "Georgene", "Georgeta", "Georgette", "Georgia", "Georgiana", "Georgianna", "Georgina", "Georgine", "Geovanna", "Géraldine",
            "Geraldine", "Gerarda", "Gerd", "Gerda", "Gerli", "Germana", "Gerrie", "Gertie", "Gertruda", "Gertrude", "Gesche", "Gesina", "Gesine", "Gessica",
            "Getter", "Ghada", "Ghalia", "Ghazala", "Ghislaine", "Gia", "Giada", "Gianina", "Gianna", "Giedrė", "Gigliola", "Gila", "Gilberte", "Gillian", "Gimena",
            "Gina", "Ginevra", "Ginko", "Ginny", "Gintarė", "Giorgia", "Giovanna", "Gisela", "Gisele", "Gisèle", "Gisella", "Giselle", "Gisken", "Gita", "Gitanjali",
            "Githa", "Gitte", "Giulia", "Giuliana", "Giulietta", "Giuseppina", "Gizem", "Gladys", "Glaiza", "Glaphyra", "Glenda", "Glenna", "Glennis", "Glenys",
            "Glória", "Gloria", "Gloriana", "Glynis", "Goggi", "Gökçe", "Gökçen", "Göksu", "Göksun", "Golda", "Gołda", "Goldie", "Golnar", "Gönül", "Gonxha",
            "Gorana", "Gordana", "Goretti", "Görkem", "Gormflaith", "Göta", "Gözde", "Grace", "Graciela", "Gracy", "Gráinne", "Gratia", "Grayce", "Grazia",
            "Graziella", "Gražina", "Grażyna", "Greca", "Greet", "Greta", "Gretchen", "Grete", "Gretel", "Gretta", "Grietje", "Griselda", "Grit", "Grizel", "Gro",
            "Grozdana", "Guðbjörg", "Guðlaug", "Guðrún", "Gudrun", "Guendalina", "Gugulethu", "Guinevere", "Guiomar", "Guiying", "Gul", "Gülbahar", "Gülcan",
            "Gülçin", "Güler", "Gulmira", "Gülşah", "Gülşen", "Gülsüm", "Gun", "Gunda", "Gundega", "Gunhild", "Gunilla", "Gunn", "Gunnel", "Günseli", "Gunta",
            "Gurandukht", "Gurli", "Gussie", "Gustava", "Güzin", "Gwen", "Gwenda", "Gwendolen", "Gwendoline", "Gwendolyn", "Gwenffrewi", "Gwenllian",
            "Gwladys", "Gwyneth", "Gyda", "Gyöngyi", "Habiba", "Hadia", "Hafdís", "Hafsa", "Hafsatu", "Hagar", "Haifa", "Hailie", "Haimanti", "Haisley",
            "Hajnal", "Hajra", "Hala", "Hale", "Haleh", "Haley", "Halide", "Halima", "Halla", "Halldóra", "Hallie", "Halyna", "Hamida", "Hana", "Hanae",
            "Hanako", "Hanami", "Hanan", "Handan", "Hande", "Hanifa", "Hanife", "Hanna", "Hannah", "Hanne", "Hanneke", "Hannele", "Hannelore", "Hansje",
            "Harika", "Harmony", "Harpreet", "Harriet", "Harshita", "Harue", "Haruhi", "Haruko", "Haruna", "Haruno", "Haruyo", "Hasibe", "Hasmik", "Hasna",
            "Hasret", "Hasumi", "Hatice", "Hatidža", "Hatsue", "Hatsuko", "Hatsumi", "Hatsune", "Haukje", "Havana", "Havva", "Hawa", "Hayal", "Hayat",
            "Haydée", "Hayden", "Hayley", "Hazal", "Hazan", "Hazel", "Hazelle", "Heather", "Heba", "Hedda", "Hédi", "Hedvig", "Hedwig", "Hedy", "Hege",
            "Heide", "Heidemarie", "Heidi", "Heidrun", "Heini", "Hele", "Heleen", "Helen", "Helena", "Helene", "Helga", "Helge", "Heli", "Helia", "Helie", "Heljo",
            "Helju", "Helle", "Helma", "Helmi", "Heloise", "Helvi", "Hemalata", "Hemlata", "Henda", "Hendrika", "Hengameh", "Henna", "Hennie", "Henny",
            "Henrietta", "Henriette", "Henriëtte", "Henrika", "Henrike", "Henuttawy", "Herlinde", "Hermina", "Hermine", "Herminia", "Hermione", "Hero",
            "Herta", "Hertha", "Hessa", "Hessy", "Hester", "Hetepheres", "Hetty", "Hiam", "Hiba", "Hibari", "Hideko", "Hila", "Hilal", "Hilary", "Hilda", "Hilde",
            "Hildegard", "Hildr", "Hildur", "Hilja", "Hilkka", "Hilla", "Hilma", "Himashree", "Himawari", "Himika", "Himiko", "Hina", "Hinako", "Hind", "Hira",
            "Hiroe", "Hiroka", "Hiroko", "Hiroyo", "Hisa", "Hisae", "Hisako", "Hisayo", "Hitomi", "Hiyori", "Hjördís", "Hoda", "Hodan", "Hodierna", "Hokuma",
            "Holly", "Hólmfríður", "Honami", "Honoka", "Honor", "Hope", "Hortense", "Hoshiko", "Houda", "Houkje", "Hrafnhildur", "Hrefna", "Hristina", "Huda",
            "Huguette", "Huhana", "Hulda", "Hülya", "Humaira", "Hunter", "Hyacinth", "Hypatia", "Iben", "Ibijoke", "Ibtisam", "Ibtissam", "Ichigo", "Ichiko",
            "İclal", "Ida", "İdil", "Idina", "Idoia", "Ieva", "Iffat", "Ifigeneia", "Ifunanya", "Ignacia", "Iheoma", "Iiris", "Ikue", "Ikuko", "Ikumi", "Ikura", "Ikuyo", "Ila",
            "Ilana", "Ilaria", "İlayda", "Ildikó", "Ileana", "Ilektra", "Ilene", "Ilenia", "Ilinca", "Ilka", "Ilke", "Ilmi", "Ilona", "Ilonka", "Ilse", "Ilyana", "Ilza", "Ilze",
            "Iman", "Imbi", "Imelda", "Imogen", "Ina", "Ina", "Inaam", "Ināra", "Inbar", "Inday", "India", "Indira", "Indra", "Indrani", "Indrė", "Indumati", "Indya",
            "Ineke", "Ines", "Inese", "Inessa", "Ineta", "Inez", "Inga", "Ingalill", "Ingar", "Inge", "Ingeborg", "Ingegerd", "Ingelin", "Ingelise", "Inger", "Ingrid",
            "Ingrīda", "Ingrida", "Inguna", "Inji", "Inkeri", "Inmaculada", "Inna", "Inori", "Inta", "Intissar", "Io", "Ioana", "Ioanna", "Iola", "Iolanda", "Iona",
            "Ionela", "Ionica", "İpek", "Iphigenia", "Iphigénie", "Ippolita", "Iqra", "Irada", "Irati", "Irbe", "İrem", "Iren", "Irena", "Irene", "Iria", "Iriana", "Irina",
            "Irinel", "Iris", "Irit", "Irja", "Irma", "Irmak", "Irmela", "Irmgard", "Iroha", "Isa", "Isabel", "Isabella", "Isannah", "Iselilja", "Iselin", "İsenbike", "Iset",
            "Ishika", "Isidora", "Işıl", "Işın", "Isis", "Isla", "Isobel", "Isoko", "Isola", "Isolde", "Isuzu", "Ita", "Italia", "Ito", "Itsuko", "Itsumi", "Itziar", "Iulia",
            "Iuliana", "Iva", "Ivaana", "Ivalu", "Ivana", "Ivelisse", "Iveta", "Ivett", "Ivette", "Ivica", "Ivita", "Ivone", "Ivonne", "Ivy", "Iwako", "Iwona", "Iyo",
            "Izabela", "Izabella", "Izaro", "İzel", "Izetta", "Izolda", "Jaana", "Jabulile", "Jacin", "Jacinta", "Jacinthe", "Jack", "Jackie", "Jaclyn", "Jacoba",
            "Jacobine", "Jacquelin", "Jacqueline", "Jacquetta", "Jacqui", "Jacquie", "Jada", "Jade", "Jaden", "Jadranka", "Jadwiga", "Jagna", "Jagoda",
            "Jahanara", "Jaime", "Jaklin", "Jale", "Jamie", "Jamila", "Jamileh", "Jan", "Jana", "Janaki", "Jane", "Janee", "Janelle", "Janet", "Janey", "Janica",
            "Janice", "Janie", "Janina", "Janiya", "Janne", "Janneke", "January", "Jarmila", "Jaroslava", "Jarosława", "Jasia", "Jasleen", "Jasmina", "Jasmine",
            "Jasna", "Javiera", "Jawahir", "Jay", "Jayda", "Jayden", "Jayne", "Jaynie", "Jazlyn", "Jean", "Jeana", "Jeananne", "Jeanette", "Jeanie", "Jeanine",
            "Jeanne", "Jeannie", "Jehanne", "Jelena", "Jemima", "Jemma", "Jen", "Jena", "Jenn", "Jenna", "Jenni", "Jennica", "Jennifer", "Jenny", "Jensen",
            "Jerri", "Jerrie", "Jerry", "Jess", "Jessa", "Jessalyn", "Jessica", "Jessie", "Jet", "Jette", "Jill", "Jillian", "Jilly", "Jimena", "Jindřiška", "Jinny",
            "Jiřina", "Jitka", "Jitsuko", "Jo", "Joan", "Joani", "Joanie", "Joanna", "Joanne", "Joaquina", "JoBeth", "Jocelyn", "Jocelyne", "Jodi", "Jodie", "Jody",
            "Joelle", "Joëlle", "Joey", "Johanna", "Johnnie", "Johnny", "Joice", "Joie", "Joke", "Jolana", "Jolanda", "Jolanta", "Jolene", "Jolie", "Jolien", "Jolijn",
            "Jonell", "Jonelle", "Jónína", "Jordan", "Jordana", "Jorien", "Jorja", "Jorun", "Jorunn", "Josefa", "Josefin", "Josefina", "Josefine", "Josepha",
            "Josephina", "Josephine", "Josette", "Joshna", "Josiane", "Josie", "Joumana", "Jouri", "Jovana", "Joy", "Joya", "Joyce", "Juana", "Juanita", "Judi",
            "Judie", "Judit", "Judita", "Judith", "Judy", "Judy", "Juhi", "Julia", "Juliana", "Juliane", "Juliann", "Julianna", "Julianne", "Julie", "Julie-Marie",
            "Juliet", "Julieta", "Juliette", "Julija", "Julissa", "Jumana", "June", "June", "Juniper", "Junko", "Juno", "Jūratė", "Jurga", "Jurgita", "Juri", "Justina",
            "Justine", "Justyna", "Jutta", "Jytte", "Kaarina", "Kacey", "Kacie", "Kader", "Kadi", "Kadia", "Kadri", "Kadriye", "Kaho", "Kahori", "Kahoru", "Kai",
            "Kaia", "Kaidi", "Kaija", "Kailey", "Kaili", "Kaire", "Kairi", "Kaisa", "Kaiva", "Kaja", "Kajsa", "Kako", "Kalina", "Kalla", "Kalsoom", "Kamie", "Kamilla",
            "Kana", "Kanako", "Kanami", "Kanchana", "Kanerva", "Kaneza", "Kanika", "Kanishka", "Kanna", "Kano", "Kanoko", "Kanon", "Kaori", "Kaoruko",
            "Kara", "Karan", "Kareena", "Karen", "Kari", "Karien", "Karima", "Karin", "Karina", "Karine", "Karla", "Karlee", "Karlene", "Karli", "Karlie", "Karlijn",
            "Karlina", "Karline", "Karly", "Karmele", "Karola", "Karolien", "Karoliina", "Karolin", "Karolina", "Karolyn", "Karrie", "Karsu", "Kärt", "Karthika",
            "Karyn", "Karyne", "Kasey", "Kashani", "Kasia", "Kasumi", "Kata", "Katalin", "Katariina", "Katarina", "Katarzyna", "Katay", "Kate", "Kateri",
            "Katerina", "Katey", "Kath", "Käthe", "Katherine", "Kathleen", "Kathlyn", "Kathryn", "Kathy", "Kati", "Katia", "Katica", "Katie", "Katina", "Katja",
            "Kätlin", "Katri", "Katrin", "Katrín", "Katrina", "Katryna", "Katsuko", "Katsura", "Katsuyo", "Katy", "Katya", "Kavita", "Kawai", "Kay", "Kaya", "Kaye",
            "Kayla", "Kayle", "Kaylee", "Kayleigh", "Kaylin", "Kayoko", "Kazimiera", "Kazue", "Kazuha", "Kazuko", "Kazusa", "Kazuyo", "Kea", "Keerthi", "Keiki",
            "Keiko", "Keira", "Keisha", "Kelly", "Kelsey", "Kendra", "Kerly", "Kerrie", "Kersti", "Kerstin", "Kerttu", "Kertu", "Keshia", "Ketevan", "Ketlin", "Kezban",
            "Khadija", "Khadra", "Khady", "Khairunnisa", "Khaleda", "Khaleesi", "Khanyisile", "Khatereh", "Khatia", "Khawla", "Khawlah", "Khethiwe", "Khioniya",
            "Khorshid", "Khrystyna", "Kiana", "Kianna", "Kiara", "Kie", "Kiera", "Kierra", "Kiersten", "Kiho", "Kiiko", "Kikelomo", "Kikki", "Kiko", "Kiku", "Kikue",
            "Kikuko", "Kim", "Kimberley", "Kimi", "Kimia", "Kimika", "Kimiko", "Kimiyo", "Kinneret", "Kinu", "Kinuko", "Kira", "Kirari", "Kirie", "Kirika", "Kiriko",
            "Kirino", "Kirsi", "Kirsteen", "Kirsten", "Kirsti", "Kirstin", "Kirsty", "Kirstyn", "Kirtan", "Kisato", "Kishwer", "Kitty", "Kiyoe", "Kiyoko", "Kiyomi",
            "Kiyone", "Kizuna", "Kjersti", "Kjerstin", "Klaartje", "Klaudia", "Klavdiya", "Kleoniki", "Kohana", "Koharu", "Koko", "Kolbrún", "Komako", "Konami",
            "Konca", "Kono", "Konoha", "Konomi", "Konstantina", "Kornelia", "Korneliya", "Koruri", "Kotoe", "Kotoko", "Kotomi", "Kotono", "Kotori", "Kou",
            "Kozue", "Krista", "Kristel", "Kristen", "Kristi", "Kristiana", "Kristiina", "Kristin", "Kristina", "Kristine", "Kristy", "Kristyn", "Kristýna", "Krisztina",
            "Krysia", "Krysten", "Krystina", "Krystle", "Krystyna", "Kshama", "Kubra", "Kujtime", "Külli", "Kulthum", "Kumi", "Kumiko", "Kumudini", "Kunigunde",
            "Kuniko", "Kureha", "Kuriko", "Květa", "Kylie", "Kyllikki", "Kyndra", "Kyoko", "Kyra", "Laarni", "Lacey", "Lada", "Ladina", "LaDonna", "Lærke",
            "Laetitia", "Lagle", "Lahja", "Laia", "Laima", "Laimdota", "Laine", "Lainie", "Laisa", "Lakeisha", "Lakshanya", "Lakshmi", "Lale", "Lama", "Lamia",
            "Lan", "Lana", "Lanette", "Lann", "Lanna", "Lara", "Larissa", "Lark", "Lasairfhíona", "LaShonda", "Lāsma", "Lata", "LaTanya", "Latasha", "Latha",
            "Latheefa", "Latifa", "Latife", "Latika", "Latisha", "LaTonya", "Latoya", "Laura", "Lauralee", "Lauran", "Laurel", "Lauren", "Laurence", "Laurène",
            "Lauretta", "Laurette", "Lauriane", "Laurie", "Lauryn", "Lavender", "Lavilla", "Lavina", "Lavinia", "Layal", "Layan", "Lea", "Leah", "Leana", "Leandra",
            "Leanna", "Leanne", "Leatrice", "Lee", "Leeanna", "Leela", "Leelavathi", "Leen", "Leena", "Leia", "Leida", "Leila", "Leilani", "Leire", "Leisa", "Leisha",
            "Lejla", "Lelde", "Lempi", "Lena", "Lene", "Leni", "Lenina", "Lenka", "Lenna", "Lenore", "Leona", "Leonie", "Léonie", "Leonor", "Leonora", "Leonore",
            "Leontina", "Leontine", "Léontine", "Leontyna", "Leontyne", "Leopoldine", "Leora", "Lepa", "Leposava", "Lesia", "Lesley", "Lesli", "Leslie", "Leta",
            "Leticia", "Letícia", "Letitia", "Letizia", "Lettice", "Letty", "Lexi", "Leyna", "Lí Ban", "Lia", "Líadan", "Liana", "Liane", "Lianne", "Libby", "Libuše",
            "Licia", "Liddy", "Lidia", "Lidija", "Lidy", "Lieke", "Liene", "Liepa", "Liesbeth", "Lieselotte", "Liesl", "Lieve", "Līga", "Ligia", "Liia", "Liina", "Liis",
            "Liisa", "Liisi", "Lika", "Lila", "Lili", "Lilia", "Liliana", "Liliane", "Lilias", "Lilibet", "Lilibeth", "Lilija", "Lilith", "Lilja", "Lilla", "Lilli", "Lillian", "Lillie",
            "Lilly", "Lilo", "Lilou", "Lily", "Lilyan", "Limor", "Lina", "Linda", "Lindelwa", "Lindita", "Lindiwe", "Lindsay", "Lindy", "Line", "Linet", "Linette",
            "Linnéa", "Linnie", "Linor", "Lioba", "Lis", "Lisa", "Lisabeth", "Lisanne", "Lisbeth", "Lise", "Liselott", "Liselotte", "Lisl", "Lissy", "Lita", "Liv", "Livia",
            "Liz", "Liza", "Lizeth", "Lizette", "Lizzie", "Ljiljana", "Ljuba", "Ljubica", "Ljupka", "Loda", "Loes", "Logan", "Loida", "Lois", "Lola", "Lolita", "Lone",
            "Loni", "Lonneke", "Loraine", "Loredana", "Lorelei", "Lorena", "Lorenza", "Loreta", "Loretta", "Lori", "Lorinda", "Lorna", "Lorraine", "Lorrane",
            "Lorrayne", "Lorrie", "Lota", "Lotta", "Lotte", "Lotten", "Lotti", "Lottie", "Lotty", "Louane", "Louella", "Louisa", "Louise", "Loula", "Lourdes", "Love",
            "Lovisa", "Lowiena", "Lowri", "Luana", "Luana", "Luanne", "Lubna", "Luca", "Luce", "Lucero", "Luci", "Lúcia", "Lucia", "Luciana", "Lucie", "Lucienne",
            "Lucija", "Lucinda", "Lucretia", "Lucrezia", "Lucy", "Ludivine", "Ludmila", "Ludovica", "Ludwika", "Luigia", "Luigina", "Luisa", "Luisana", "Luitgard",
            "Luiza", "Luknė", "Lulah", "Luljeta", "Lulwa", "Luminița", "Luna", "Lungiswa", "Lupe", "Lupita", "Lurleen", "Lurline", "Lusine", "Lutfiya", "Lütfiye",
            "Luule", "Luyun", "Luz", "Luzviminda", "Lyda", "Lydia", "Lynda", "Lyndal", "Lyndsay", "Lynnette", "Lyra", "Lysette", "Lyubov", "Maaike", "Maarit",
            "Maarja", "Maartje", "Maaya", "Mabel", "Mable", "Macarena", "Machi", "Machiko", "Macy", "Madalena", "Mădălina", "Maddy", "Madelaine",
            "Madeleine", "Madelyn", "Madge", "Madhabi", "Madhavi", "Madhuri", "Madiha", "Madison", "Madjiguène", "Madoka", "Madonna", "Mae", "Maëlys",
            "Maeva", "Maeve", "Magda", "Magdalena", "Magdalene", "Maggie", "Magnhild", "Magnolia", "Maha", "Mahasweta", "Mahaut", "Mahboubeh",
            "Mahfuza", "Mahiro", "Mahiru", "Mahnaz", "Mahnoosh", "Maho", "Mahsa", "Mahshid", "Mahtab", "Mahulena", "Mai", "Maia", "Maiara", "Maibritt",
            "Maida", "Maika", "Maiko", "Maila", "Maimi", "Mair", "Máire", "Mairead", "Maisie", "Maite", "Maja", "Majda", "Majella", "Majka", "Makhosazana",
            "Maki", "Makiko", "Malani", "Malathi", "Maleka", "Małgorzata", "Małgosia", "Maliha", "Malika", "Malin", "Mălina", "Mall", "Malla", "Malle", "Mallerie",
            "Mallika", "Mallory", "Malou", "Malti", "Malvina", "Mami", "Mamiko", "Mamizu", "Mana", "Manaka", "Manal", "Manami", "Manana", "Mandana",
            "Mandisa", "Mandy", "Maneet", "Maneh", "Manijeh", "Manike", "Manila", "Manisha", "Manjula", "Manola", "Manolita", "Manon", "Manorama",
            "Manuéla", "Manuela", "Māra", "Mara", "Marat", "Marcela", "Marceline", "Marcella", "Marcellina", "Marcia", "Marcie", "Mare", "Maree", "Mareile",
            "Marella", "Maren", "Maret", "Marfa", "Marg", "Marga", "Margalit", "Margalo", "Margaret", "Margareta", "Margarete", "Margaretha", "Margarethe",
            "Margaretta", "Margarida", "Margarita", "Margaux", "Marge", "Margherita", "Margie", "Margit", "Margo", "Margot", "Margrethe", "Margriet", "Margrit",
            "Marguerite", "Margy", "Mari", "Mária", "Maria", "Mariah", "Mariam", "Mariama", "Mariamne", "Marian", "Mariana", "Mariann", "Marianne", "Mariasole",
            "Maribel", "Maricel", "Maricica", "Marie", "Marieke", "Mariel", "Mariela", "Mariella", "Marielle", "Marigold", "Marigold", "Marija", "Marijana", "Marije",
            "Marijke", "Marijn", "Marika", "Mariko", "Marilena", "Marilu", "Marilyn", "Marin", "Marina", "Marine", "Marinette", "Marioara", "Marion", "Maris",
            "Marisa", "Marisela", "Mariska", "Marisol", "Marissa", "Marit", "Marita", "Marivic", "Mariya", "Mariz", "Marj", "Marja", "Marjan", "Marjana", "Marjatta",
            "Marji", "Marjie", "Marjo", "Marjolein", "Marjon", "Marjorie", "Marjory", "Marju", "Marjut", "Markéta", "Marlana", "Marlee", "Marleen", "Marlen",
            "Marlene", "Marlies", "Marlise", "Marloes", "Marnie", "Marsha", "Märta", "Marta", "Martha", "Marthe", "Martina", "Martine", "Maru", "Maruja",
            "Marumi", "Maruša", "Maruxa", "Marwa", "Mary", "Maryam", "Maryanne", "Maryka", "Maryla", "Maryse", "Maryvonne", "Marzena", "Marzia",
            "Marzieh", "Masae", "Masako", "Masayo", "Maserame", "Masha", "Mashiro", "Masoumeh", "Masuko", "Masuma", "Matea", "Mateja", "Matilda",
            "Matilde", "Matryona", "Matsuko", "Matsuri", "Maud", "Maud", "Maude", "Maura", "Maureen", "Maurette", "Maurine", "Mavis", "Maxine", "Maxine",
            "May", "Maya", "Mayako", "Mayara", "Maybelle", "Mayme", "Maymuna", "Mayo", "Mayola", "Maysoon", "Mayu", "Mayuka", "Mayuko", "Mayumi",
            "Mbalenhle", "Mbali", "McKenna", "Meara", "Meaza", "Mebrure", "Mechthild", "Medb", "Medea", "Medina", "Medora", "Meeli", "Megan", "Meggie",
            "Meghana", "Meghna", "Megu", "Megumi", "Mehitable", "Mehrangiz", "Mehreen", "Mehtap", "Mei", "Meike", "Meiko", "Meiling", "Meirav", "Meisa",
            "Mekdes", "Mel", "Melania", "Melanie", "Mélanie", "Meleana", "Meleane", "Melek", "Melia", "Meliha", "Melike", "Melina", "Melinda", "Melis", "Melisa",
            "Melissa", "Melita", "Mellisa", "Melly", "Melody", "Melody", "Meltem", "Mendy", "Menike", "Meral", "Mercan", "Mercè", "Mercedes", "Merceline",
            "Mercy", "Meredith", "Merel", "Meresankh", "Merete", "Meri", "Merike", "Merilyn", "Merima", "Meritamen", "Meritites", "Meritxell", "Merja", "Merle",
            "Merline", "Merrilyn", "Merve", "Meryem", "Meseret", "Meta", "Metta", "Mette", "Mhairi", "Mia", "Micah", "Michaela", "Michela", "Michele",
            "Micheline", "Michelle", "Michi", "Michie", "Michiko", "Mickey", "Midori", "Mie", "Mieczysława", "Mieke", "Mieko", "Mietje", "Migdalia", "Mignon",
            "Mignonne", "Mihaela", "Miharu", "Miho", "Mihoko", "Miiko", "Miina", "Mika", "Mikako", "Miki", "Mikiko", "Mikoto", "Miku", "Mikuni", "Mikuru", "Mila",
            "Milada", "Milagros", "Milda", "Mildred", "Milena", "Miley", "Milica", "Milka", "Millaray", "Millia", "Millicent", "Millie", "Milly", "Miluše", "Milva", "Milvi",
            "Mima", "Mimi", "Mimmi", "Mimori", "Mina", "Minae", "Minako", "Minami", "Minase", "Minatsu", "Minayo", "Mindi", "Mindy", "Mine", "Minea", "Mineke",
            "Mineko", "Minerva", "Mingzhu", "Minna", "Minnie", "Minoo", "Minou", "Mio", "Mioko", "Mion", "Miori", "Mira", "Mirabel", "Miral", "Miran", "Miranda",
            "Miray", "Mirdza", "Mireia", "Mireille", "Mirela", "Mirella", "Miren", "Miri", "Miria", "Miriam", "Mirit", "Mirja", "Mirjam", "Mirjana", "Mirka", "Mirna",
            "Miroslava", "Mirosława", "Mirsada", "Mirta", "Mirtha", "Miru", "Misa", "Misae", "Misaki", "Misako", "Misato", "Mishaal", "Misono", "Missy", "Misty",
            "Misumi", "Misuzu", "Mithu", "Mitoyo", "Mitra", "Mitsuba", "Mitsuki", "Mitsuko", "Mitsuyo", "Mittie", "Mitzi", "Miu", "Miwa", "Miwako", "Miya",
            "Miyabi", "Miyako", "Miye", "Miyo", "Miyoko", "Miyoshi", "Miyū", "Miyuki", "Miyumi", "Mizue", "Mizuko", "Mmabatho", "Moa", "Moe", "Moeka",
            "Moeko", "Mohini", "Moira", "Mojca", "Molly", "Momiji", "Momo", "Momoe", "Momoha", "Momoka", "Momoko", "Momona", "Mona", "Mone", "Monica",
            "Monika", "Moninne", "Monique", "Monna", "Montserrat", "Moonika", "Mór", "Morena", "Morenike", "Morfudd", "Morgan", "Moriah", "Morna",
            "Morwenna", "Motoko", "Mouna", "Moushumi", "Moya", "Moyra", "Mozhdeh", "Mozhgan", "Mrinalini", "Muazzez", "Mudrīte", "Muffy", "Müge", "Mugi",
            "Muguette", "Muire", "Muireann", "Müjde", "Muneeba", "Munira", "Murasaki", "Muriel", "Murielle", "Mutsuko", "Mutsumi", "Myfanwy", "Mylene",
            "Myra", "Myriane", "Myrna", "Myrthe", "Myrtle", "Naana", "Nabahat", "Nabila", "Nachimi", "Nada", "Nadeesha", "Nadège", "Nadezhda", "Nadia",
            "Nadica", "Nadine", "Nadira", "Nadiya", "Nadja", "Nadya", "Nadzeya", "Nafisa", "Nafissa", "Nagako", "Nagehan", "Naghma", "Nahia", "Nahla", "Naho",
            "Nahomi", "Naiara", "Naika", "Naila", "Naima", "Naiomi", "Naira", "Nairanjana", "Najat", "Najwa", "Nako", "Nalan", "Nalini", "Nami", "Namie", "Namiko",
            "Namrata", "Nana", "Nanae", "Nanaka", "Nanako", "Nanami", "Nanase", "Nanci", "Nancy", "Nandita", "Nanette", "Nanne", "Nannerl", "Nao", "Naoko",
            "Naomi", "Narcissa", "Nareh", "Nargess", "Nariman", "Narimi", "Narine", "Naru", "Naruko", "Narumi", "Nashla", "Nasim", "Nasira", "Nasrin", "Nastja",
            "Nasya", "Natacha", "Natalee", "Natali", "Natalia", "Natalie", "Nataliia", "Natālija", "Nataliya", "Natalka", "Natallia", "Nataly", "Natalya", "Nataša",
            "Natasha", "Natela", "Natella", "Nathalie", "Natia", "Natsue", "Natsuko", "Natsume", "Natsumi", "Nava", "Navjeet", "Nawal", "Nawoja", "Nayla",
            "Nayoko", "Nazan", "Nazanin", "Nazaret", "Nazia", "Naziha", "Nazira", "Nazli", "Ndeye", "Nea", "Neaera", "Nebahat", "Nechama", "Necla", "Nedda",
            "Nedra", "Neela", "Neelam", "Neera", "Neeta", "Neetu", "Neferu", "Negar", "Negin", "Neha", "Nehal", "Nehir", "Neila", "Nejla", "Neko", "Nel", "Nela",
            "Nelia", "Nell", "Nella", "Nelli", "Nelly", "Nena", "Nene", "Nerea", "Neringa", "Nerissa", "Nermin", "Neru", "Nerys", "Neşe", "Neshat", "Neslihan",
            "Nessa", "Netsanet", "Nettie", "Netty", "Neva", "Nevaeh", "Nevena", "Nevenka", "Nevin", "Nezha", "Nezihe", "Ngahuia", "Nia", "Niamh", "Nichi",
            "Nichole", "Nicholeen", "Nicki", "Nicola", "Nicolasa", "Nicole", "Nicolene", "Nicoleta", "Nicoletta", "Nicolle", "Niculina", "Nida", "Nidaa", "Nidhi",
            "Nidia", "Nienke", "Nieves", "Nihal", "Nihan", "Niharika", "Niina", "Nijolė", "Nika", "Nike", "Nikita", "Nikola", "Nikoleta", "Nikoletta", "Nikolina",
            "Nikta", "Nil", "Nilay", "Nilda", "Nilgün", "Nili", "Nilmini", "Niloufar", "Nilüfer", "Nimali", "Nimisha", "Nina", "Ninel", "Ninetta", "Ninette", "Nino",
            "Ninon", "Nisha", "Nishi", "Niusha", "Nivea", "Nivetha", "Nivi", "Nkechi", "Nkem", "Nnenna", "Noa", "Nobue", "Nobuhle", "Nobuko", "Nodoka", "Noel",
            "Noela", "Noelia", "Noelie", "Noeline", "Noella", "Noelle", "Noémie", "Nóirín", "Nokwethemba", "Nolwazi", "Nolwenn", "Nomalanga", "Nomathemba",
            "Nombulelo", "Nompumelelo", "Nomthandazo", "Nomvula", "Nomzamo", "Non", "Nona", "Nonceba", "Nondumiso", "Nonhlanhla", "Nonkululeko",
            "Nonna", "Nonoka", "Noora", "Nora", "Noreen", "Norica", "Noriko", "Noriyo", "Norma", "Nothando", "Noura", "Nouria", "Noxolo", "Noya", "Nthabiseng",
            "Nuala", "Nubia", "Nunzia", "Nupur", "Nur ul-Huda", "Nuraini", "Nuran", "Nuray", "Nurcan", "Nurgül", "Nuria", "Núria", "Nursel", "Nuta", "Nutsa",
            "Nuzhat", "Nwando", "Nzinga", "Oana", "Océane", "Octavia", "Oddny", "Odelia", "Odette", "Odie", "Odile", "Ofuafo", "Ogonna", "Oihane", "Oksana",
            "Ola", "Ólafía", "Olea", "Olena", "Olesya", "Olga", "Olgica", "Olha", "Olimpiada", "Oline", "Olive", "Olivera", "Olivette", "Olívia", "Olivia", "Oliwia",
            "Olja", "Olwen", "Olympia", "Olympias", "Oma", "Omolara", "Ona", "Õnne", "Onóra", "Oona", "Opal", "Ophelia", "Orelia", "Oriana", "Orietta", "Orion",
            "Orit", "Orla", "Órlaith", "Orli", "Ornella", "Orsolya", "Ortrud", "Otilia", "Oto", "Otoha", "Otome", "Ottavia", "Ottilie", "Oumayma", "Outi", "Oveta",
            "Oya", "Öykü", "Oylum", "Özge", "Özgü", "Özgül", "Özlem", "Öznur", "Pablita", "Paddy", "Padmaja", "Padmavati", "Pádraigín", "Paige", "Päivi",
            "Palak", "Palesa", "Pallavi", "Palmer", "Palmira", "Paloma", "Pam", "Pamela", "Pamelyn", "Panagiota", "Pania", "Panorea", "Pansy", "Pantea",
            "Paola", "Paoletta", "Papiya", "Paquita", "Paraskevi", "Paris", "Parisa", "Parvaneh", "Parvati", "Parveen", "Pascale", "Patience", "Patrice",
            "Patricia", "Patrizia", "Patsy", "Patty", "Paula", "Paule", "Paulette", "Paulien", "Paulina", "Pauline", "Pavithra", "Pavla", "Payton", "Peaches",
            "Pearl", "Pegah", "Pegeen", "Peggy", "Pelin", "Penda", "Penelope", "Penny", "Pepper", "Peppi", "Perdita", "Perica", "Perihan", "Perl", "Perle",
            "Pernette", "Pernilla", "Pernille", "Perrine", "Perry", "Persia", "Persis", "Pervin", "Pesya", "Peta", "Petra", "Petrina", "Petronella", "Petula",
            "Petunia", "Phebe", "Phia", "Philippa", "Philomena", "Phoebe", "Phumzile", "Phyllida", "Phyllis", "Pia", "Piera", "Pierina", "Pierrette", "Pihla",
            "Piia", "Pilar", "Pille", "Pina", "Pinar", "Pipaluk", "Piper", "Pippa", "Piret", "Pirjo", "Pirkko", "Piroska", "Pixie", "Pleasance", "Pnina", "Poli", "Polina",
            "Polly", "Polona", "Poonam", "Poppy", "Porntip", "Portia", "Posy", "Poulomi", "Pranati", "Praskovya", "Pratibha", "Pratiksha", "Precious", "Preeti",
            "Prerna", "Primrose", "Prisca", "Priscila", "Priscilla", "Priska", "Priya", "Priyani", "Priyanka", "Prudence", "Prunella", "Publia", "Puck", "Puja",
            "Purita", "Qingling", "Quanita", "Queenie", "Quendrida", "Queralt", "Quiana", "Quinn", "Rabeya", "Rabia", "Rachel", "Rada", "Radina", "Radka",
            "Radmila", "Radoslava", "Radostin", "Rae", "Raewyn", "Raffaella", "Raghnailt", "Ragna", "Ragne", "Ragnhild", "Rahaf", "Rahel", "Rahima", "Rahma",
            "Raijieli", "Raili", "Raimonda", "Rain", "Raine", "Raisa", "Rajathi", "Rakel", "Raleigh", "Raluca", "Rambha", "Raminta", "Ramita", "Ramona", "Ramunė",
            "Ramya", "Ran", "Randi", "Randy", "Rangina", "Rani", "Rania", "Ranjeeta", "Ranko", "Rannveig", "Ranveig", "Ranze", "Raquel", "Rasa", "Rasha",
            "Rashida", "Rashmi", "Rashmika", "Rasma", "Rati", "Raven", "Rawda", "Raya", "Raymonde", "Rayna", "Rayssa", "Razia", "Razia Sultana", "Reanna",
            "Reba", "Rebeca", "Rebecca", "Rebecka", "Reda", "Reem", "Reema", "Reet", "Regiane", "Regina", "Regina", "Regine", "Régine", "Reham", "Rehana",
            "Reika", "Reiko", "Reina", "Reira", "Réka", "Rekha", "Remi", "Remziye", "Rena", "Renata", "Renate", "Renée", "Renesmee", "Renita", "Renitta",
            "Renske", "Reona", "Retha", "Rethabile", "Rewan", "Reyhan", "Reyna", "Rhea", "Rhian", "Rhiannon", "Rhoda", "Rhodogune", "Rhona", "Rhonda",
            "Ria", "Rianne", "Ricarda", "Richardis", "Richelle", "Richeza", "Ridhima", "Rie", "Rieko", "Riffat", "Riho", "Rihoko", "Riin", "Riina", "Rika", "Rikako",
            "Rikiko", "Rikka", "Rikke", "Riko", "Riley", "Rimantė", "Rimas", "Rimma", "Rina", "Rinako", "Ringo", "Rinka", "Rinko", "Rinne", "Rino", "Riri", "Riria",
            "Risa", "Risako", "Risë", "Rissi", "Rita", "Ritsuko", "Ritva", "Ritwika", "Rivka", "Riya", "Roberta", "Robin", "Robinah", "Rochelle", "Rocío", "Roda",
            "Rodica", "Rohini", "Róisín", "Rojbin", "Rolanda", "Romana", "Romane", "Romilda", "Romina", "Ronela", "Ronja", "Rønnaug", "Ronnia", "Ronnie",
            "Roopa", "Roos", "Rosa", "Rosabel", "Rosalba", "Rosaleen", "Rosalia", "Rosalie", "Rosalind", "Rosalinda", "Rosalyn", "Rosamaria", "Rosamond",
            "Rosamund", "Rosanna", "Rosaria", "Rosario", "Rose", "Roseanne", "Roselinda", "Rosemary", "Rosetta", "Roshanak", "Roshanna", "Rosie", "Rosina",
            "Rosine", "Rosita", "Rossana", "Rossella", "Rotha", "Rowan", "Roxana", "Roxann", "Roxanne", "Roya", "Rózsa", "Rubina", "Ruby", "Rudaba", "Ruka",
            "Rukmani", "Rukmini", "Ruma", "Rümeysa", "Rumi", "Rumiko", "Rumina", "Runa", "Ruqayya", "Ruri", "Ruriko", "Ruslana", "Russi", "Rusudan", "Rut",
            "Rūta", "Ruta", "Ruth", "Ruthie", "Rutt", "Ruxandra", "Ruža", "Růžena", "Ružica", "Ryann", "Ryouka", "Ryouko", "Saadia", "Saana", "Saara", "Saba",
            "Sabahat", "Sabiha", "Sabina", "Sabine", "Sabra", "Sabrina", "Sabriye", "Sachi", "Sachie", "Sachika", "Sachiko", "Sachimi", "Sachini", "Sachiyo",
            "Sada", "Sadaf", "Sadako", "Sadb", "Sadhbh", "Sadia", "Sadie", "Sae", "Saeko", "Safiya", "Safiye", "Sagarika", "Sahar", "Saho", "Saida", "Saidat",
            "Saija", "Saiko", "Saila", "Saima", "Saira", "Sajida", "Sakhra", "Saki", "Sakie", "Sakiho", "Sakiko", "Sakina", "Sakiyo", "Saku", "Sakuko", "Sakura",
            "Sakurako", "Saliha", "Salima", "Salimah", "Salimata", "Sally", "Sallyanne", "Salma", "Salme", "Salome", "Salomėja", "Saloni", "Salpy", "Salul",
            "Sam", "Saman", "Samaneh", "Samantha", "Samar", "Samara", "Samia", "Samiha", "Samina", "Samira", "Sana", "Sanae", "Sanah", "Sanam",
            "Sanami", "Sanaz", "Sancha", "Sanchia", "Sanda", "Sandhya", "Sandi", "Sandra", "Sandrine", "Sandy", "Sanela", "Sanem", "Sania", "Sanita",
            "Saniya", "Sanja", "Sanjana", "Sanjida", "Sanjula", "Sanna", "Sanne", "Santa", "Santina", "Saoirse", "Saori", "Sapir", "Sapphire", "Sara", "Sara",
            "Sarabeth", "Sarah", "Sarangerel", "Saranya", "Sareh", "Sari", "Sarina", "Sarit", "Sarita", "Šárka", "Sarma", "Sarmīte", "Sarojini", "Saša", "Sasha",
            "Sasikala", "Saskia", "Satoko", "Satomi", "Satsumi", "Satu", "Saturnina", "Saule", "Sava", "Savannah", "Savitri", "Savka", "Savona", "Sawa",
            "Sawako", "Sawsan", "Saya", "Sayaka", "Sayako", "Sayo", "Sayoko", "Sayori", "Sayra", "Sayuki", "Sayumi", "Sayuri", "Şaziye", "Scarlett", "Seana",
            "Şebnem", "Seçil", "Seçkin", "Seda", "Seema", "Ségolène", "Seiko", "Seina", "Seira", "Šejla", "Selda", "Selen", "Selena", "Selene", "Selin", "Selina",
            "Selma", "Selva", "Selvi", "Semiha", "Semra", "Şenay", "Senga", "Şengül", "Senko", "Sepideh", "Serafina", "Serap", "Séraphine", "Seren", "Serena",
            "Serenay", "Serenity", "Şermin", "Serpil", "Serra", "Setareh", "Setsuko", "Sevda", "Séverine", "Sevgi", "Sevil", "Sevilay", "Sevim", "Sevin", "Sevinç",
            "Şevval", "Seyran", "Sezen", "Shabana", "Shadi", "Shadia", "Shagufta", "Shahd", "Shahinaz", "Shahla", "Shailene", "Shaimaa", "Shakira", "Shakuntala",
            "Shameeka", "Shamima", "Shamsunnahar", "Shana", "Shanelle", "Shania", "Shanika", "Shaniqua", "Shantha", "Shanzay", "Shara", "Sharee", "Shari",
            "Sharla", "Sharleen", "Sharlene", "Sharmila", "Sharna", "Sharon", "Sharona", "Shashikala", "Shatha", "Shauna", "Shawna", "Shawnae", "Shawnee",
            "Shaylee", "Shayna", "Shazia", "Sheela", "Sheena", "Sheetal", "Sheila", "Sheilagh", "Shelley", "Shenna", "Sherene", "Sherin", "Sherine", "Sherrie",
            "Sherry", "Sheryl", "Sheyla", "Shiela", "Shige", "Shigeko", "Shigure", "Shiho", "Shihoko", "Shihori", "Shiina", "Shilpa", "Shimako", "Shina", "Shinako",
            "Shino", "Shiori", "Shira", "Shirin", "Shirley", "Shivangi", "Shivanna", "Shizue", "Shizuka", "Shizuko", "Shizuku", "Shizuru", "Shlomit", "Shohini",
            "Shohreh", "Shouko", "Sholeh", "Shona", "Shonda", "Shoshana", "Shpresa", "Shreya", "Shriya", "Shubha", "Shubhangi", "Shujiao", "Shuka", "Shuko",
            "Shulamith", "Shumaila", "Shweta", "Siân", "Siana", "Sibel", "Sibilla", "Sibongile", "Sibyl", "Sibylla", "Sibylle", "Sid", "Sidney", "Sidonia", "Sidra",
            "Sieglinde", "Sienna", "Sierra", "Sigita", "Signe", "Sigrid", "Sigríður", "Sigrún", "Sigurrós", "Siham", "Sihem", "Siiri", "Sikje", "Sikkelina", "Sila",
            "Síle", "Silja", "Silje", "Silke", "Sille", "Silva", "Silvana", "Silvia", "Silvija", "Silvina", "Sima", "Simge", "Simin", "Simona", "Simone", "Simonetta",
            "Simran", "Sinara", "Sindukht", "Sinéad", "Sinem", "Sini", "Sinikka", "Sinta", "Siobhan", "Síofra", "Sioned", "Siouxsie", "Siranush", "Siri", "Şirin",
            "Sirje", "Sirkka", "Sissel", "Sissela", "Sissy", "Síthmaith", "Siv", "Sivali", "Siwan", "Sjoukje", "Sky", "Skye", "Skyler", "Slađana", "Slava", "Slavena",
            "Slavica", "Slavomira", "Sławomira", "Sloane", "Smaranda", "Smilja", "Sneha", "Snežana", "Snezhana", "Sniedze", "Sofie", "Sofija", "Sofiya",
            "Soha", "Soheila", "Soheir", "Soile", "Sokhna", "Solange", "Soledad", "Solène", "Sóley", "Solfrid", "Solmaz", "Solveig", "Somayeh", "Sona", "Sonali",
            "Sonata", "Songül", "Sonia", "Sonika", "Sonja", "Sono", "Sonoko", "Sophia", "Sophie", "Sophonisba", "Sophronia", "Sophy", "Sorana", "Soraya",
            "Sorcha", "Sorina", "Sorrel", "Sotiria", "Soudabeh", "Sousan", "Souzan", "Soyini", "Spring", "Spring", "Sreelekha", "Sristi", "Sriyani", "Stacy",
            "Stamatia", "Stanislava", "Stefana", "Ștefania", "Stefania", "Steffi", "Stefi", "Stefka", "Štefka", "Steinunn", "Stela", "Stella", "Steph", "Stephanie",
            "Stéphanie", "Stephie", "Stevie", "Stina", "Stine", "Storm", "Sude", "Sudha", "Sue", "Sueko", "Suellen", "Sugako", "Suhani", "Sujata", "Şükriye",
            "Sulekha", "Sulochana", "Sultana", "Sumako", "Sumaya", "Sümeyye", "Sumi", "Sumie", "Sumika", "Sumiko", "Sumire", "Summer", "Sumru", "Suna",
            "Sunaho", "Sunila", "Sunisa", "Sunniva", "Surangani", "Susan", "Susana", "Susanna", "Susannah", "Susanne", "Sushma", "Susila", "Susmita",
            "Sussan", "Susy", "Sutton", "Süyümbike", "Suzan", "Suzana", "Suzanne", "Suzette", "Suzie", "Suzu", "Suzue", "Suzuka", "Suzuko", "Suzuna",
            "Suzy", "Svandís", "Svea", "Svenja", "Svetla", "Svetlana", "Sviatlana", "Svijetlana", "Svitlana", "Svjetlana", "Swathi", "Sybille", "Syd", "Sydney",
            "Syifa", "Sylvanie", "Sylvi", "Sylvia", "Sylvie", "Synnøve", "Szejna", "Szilvia", "Tabassum", "Tabitha", "Tae", "Taeko", "Tahira", "Tahmina",
            "Tahnee", "Tähti", "Taileflaith", "Taina", "Taisia", "Taissa", "Takako", "Takayo", "Takeko", "Takla", "Tala", "Talia", "Talisa", "Talitha", "Tallulah",
            "Tama", "Tamae", "Tamako", "Tamami", "Tamao", "Tamar", "Tamara", "Tamayo", "Tameika", "Tameka", "Tami", "Tamiko", "Tamisha", "Tammie",
            "Tammy", "Tamunotonye", "Tane", "Tanis", "Tanisha", "Tanith", "Tanja", "Tannaz", "Tansy", "Tanushree", "Tanvi", "Tanya", "Tao", "Tara", "Tarah",
            "Tarako", "Taraneh", "Tarja", "Taryn", "Tasha", "Taslima", "Tasmina", "Tasnim", "Tatsiana", "Tatsuko", "Tatiana", "Tava", "Tawny", "Taylor",
            "Tayuka", "Tazeen", "Tazmin", "Tazuko", "Téa", "Tea", "Teagan", "Tegan", "Tegwen", "Tehila", "Teiko", "Tejal", "Tejaswi", "Tejaswini", "Tekla",
            "Tema", "Temperance", "Tena", "Tenka", "Teodora", "Teofila", "Teona", "Teresa", "Teresinha", "Teresita", "Teretia", "Teréz", "Teri", "Terisa",
            "Terje", "Terry", "Terttu", "Teruko", "Teruyo", "Tesha", "Tess", "Tessa", "Tessie", "Tetsuko", "Teuntje", "Teuta", "Thais", "Thandeka", "Thandiswa",
            "Thania", "Thea", "Thekla", "Thelma", "Theodora", "Theodosia", "Theoni", "Theophano", "Theophanu", "Therese", "Thérèse", "Theresia", "Thisuri",
            "Thomasina", "Thorbjörg", "Thórdís", "Thórunn", "Tia", "Tiah", "Tiana", "Tichina", "Tiffanie", "Tiffany", "Tigerlily", "Tiia", "Tiina", "Tiiu", "Tijana",
            "Tilbe", "Tillie", "Tilly", "Tímea", "Tina", "Tinashe", "Tinatin", "Tineke", "Tingting", "Tiphanie", "Tippi", "Tiril", "Tisha", "Titilola", "Titilope", "Tiziana",
            "Tobey", "Toine", "Toinette", "Toini", "Tokie", "Tokiko", "Toko", "Tokuko", "Tomasa", "Tomie", "Tomiko", "Tómnat", "Tomoka", "Tomoko", "Tomoyo",
            "Tomris", "Tona", "Tonantzin", "Tone", "Tonette", "Toni", "Tonia", "Tonie", "Tonina", "Tonja", "Tonje", "Tonka", "Tonya", "Tonye", "Toos", "Tora",
            "Torborg", "Tordis", "Torhild", "Tori", "Torill", "Toshiko", "Toshiyo", "Tosia", "Tove", "Towe", "Toyoko", "Tracy", "Traudl", "Traute", "Trena", "Tricia",
            "Triin", "Trijn", "Trina", "Trish", "Trisha", "Trude", "Trudy", "Trupti", "Truus", "Tsehay", "Tsubaki", "Tsugumi", "Tsukiko", "Tsukushi", "Tsuneko",
            "Tsuru", "Tsuyako", "Tsveta", "Tuathflaith", "Tuba", "Tuğçe", "Tuija", "Tülay", "Tülin", "Tulsi", "Tünde", "Turid", "Türkan", "Tutta", "Tuula", "Tuuli",
            "Tuulikki", "Tuyaa", "Twyla", "Tyler", "Typhanie", "Tyra", "Tytti", "Tzipporah", "Uallach", "Uasal", "Udval", "Ugnė", "Ui", "Uki", "Uliana", "Ulla",
            "Ülle", "Ulrica", "Ulrike", "Ulrikke", "Ulvi", "Uma", "Umaria", "Ume", "Umeko", "Umi", "Umika", "Umm", "Ùna", "Una", "Unni", "Unnur", "Unoko",
            "Urraca", "Urša", "Urška", "Ursula", "Urszula", "Urtė", "Urve", "Urwa", "Uta", "Utako", "Utami", "Ute", "Utku", "Uxue", "Uzma", "Vafa", "Vahide",
            "Vaida", "Vaira", "Vaiva", "Vajira", "Val", "Valarie", "Valborg", "Valda", "Valdís", "Valeen", "Valentina", "Valentine", "Valeria", "Valerie", "Valérie",
            "Valesca", "Valgerður", "Valmai", "Valve", "Vanda", "Vanessa", "Vani", "Vanina", "Vanita", "Vanja", "Vanna", "Varalakshmi", "Varina", "Varma",
            "Varsha", "Varvara", "Vasileia", "Vasilisa", "Vassiliki", "Vega", "Velga", "Velia", "Velma", "Velma", "Velta", "Velvet", "Věnceslava", "Vendela",
            "Vendula", "Venera", "Venetia", "Venida", "Venla", "Venus", "Vera", "Vered", "Verena", "Vernice", "Verona", "Veronica", "Véronique", "Vesna",
            "Vesta", "Vibeke", "Vibha", "Vickie", "Vicky", "Victoire", "Victoria", "Vida", "Vidya", "Vieno", "Viera", "Vigdis", "Viive", "Vija", "Vijayalakshmi",
            "Vikki", "Viktorie", "Viktorija", "Viktoriya", "Vilde", "Vilija", "Vilma", "Vincenza", "Vinette", "Viola", "Violant", "Violet", "Violeta", "Violetta",
            "Violette", "Viorica", "Virág", "Virginia", "Virginie", "Virginija", "Viridiana", "Virpi", "Virve", "Vita", "Vitalia", "Vitalija", "Vittoria", "Vivalda",
            "Viveka", "Vivian", "Viviana", "Viviane", "Vlada", "Vladana", "Vladlena", "Vlasta", "Vlatka", "Vojislava", "Volha", "Voula", "Vukosava", "Wafaa",
            "Wahida", "Waka", "Wakaba", "Wakako", "Wakana", "Wako", "Waldrada", "Waltraud", "Wanda", "Warda", "Waverly", "Wednesday", "Weerts",
            "Wenche", "Wendy", "Whitney", "Widad", "Wiebke", "Wiesława", "Wiktoria", "Wilhelmina", "Willa", "Willeke", "Willemien", "Willemijn", "Willemina",
            "Willow", "Wilma", "Wiltrud", "Winifred", "Winnie", "Winnifred", "Winter", "Władysława", "Xanthe", "Xaviera", "Xenia", "Xenija", "Xiaoling",
            "Xiaoyan", "Ximena", "Xinying", "Xiomara", "Xóchitl", "Yaa", "Yachiyo", "Yadira", "Yae", "Yaeko", "Yael", "Yako", "Yamina", "Yamini", "Yana",
            "Yanar", "Yancy", "Yanet", "Yanina", "Yanmin", "Yaprak", "Yara", "Yaroslava", "Yashomati", "Yasmin", "Yasue", "Yasuko", "Yayoi", "Yazmin",
            "Yeganeh", "Yehudit", "Yekaterina", "Yekta", "Yelda", "Yelena", "Yeliz", "Yenta", "Yeşim", "Yessica", "Yetunde", "Yevheniia", "Yianna", "Ylenia",
            "Yllka", "Ylva", "Yoeko", "Yoka", "Yoko", "Yolaine", "Yolanda", "Yolande", "Yolonda", "Yoma", "Yonca", "Yordanka", "Yorgelis", "Yorie", "Yoriko",
            "Yoshiko", "Yoshino", "Yua", "Yui", "Yuika", "Yuiko", "Yuina", "Yuka", "Yukako", "Yukari", "Yukie", "Yukika", "Yukiko", "Yukimi", "Yukina",
            "Yukino", "Yukiru", "Yūko", "Yulia", "Yuliana", "Yume", "Yumei", "Yumeko", "Yumi", "Yumie", "Yumika", "Yumiko", "Yumna", "Yuna", "Yuno",
            "Yunzhu", "Yura", "Yuri", "Yuria", "Yurie", "Yurika", "Yuriko", "Yurina", "Yuumi", "Yuuna", "Yuyuko", "Yuzuki", "Yvette", "Yvonne", "Zabel",
            "Zabelle", "Zahia", "Zahida", "Zahra", "Zaidee", "Zaiga", "Zaima", "Zakiah", "Zakiya", "Zala", "Zamzam", "Zanda", "Zandra", "Zane", "Zanele",
            "Zara", "Zarela", "Zarifa", "Zarina", "Zaruhi", "Zaynab", "Zazie", "Zdena", "Zdenka", "Zdzisława", "Zeba", "Zeeshan", "Zehava", "Zeineb", "Zekiye",
            "Zelda", "Zelia", "Zélie", "Zeliha", "Željka", "Zelma", "Zena", "Zenaida", "Zenia", "Zenobia", "Zerelda", "Zerrin", "Zeta", "Zethu", "Zeynep", "Zhanna",
            "Zhazira", "Zhenxiu", "Zhenya", "Zibiah", "Zineb", "Zinnie", "Zinta", "Zita", "Ziva", "Zivia", "Živilė", "Zlata", "Zodwa", "Zoe", "Zofia", "Zohar",
            "Zohra", "Zohreh", "Zora", "Zorica", "Zorka", "Zosia", "Zośka", "Zoya", "Zsófia", "Zsuzsanna", "Zubaida", "Zuhal", "Zuhur", "Zuleika", "Zulema",
            "Zulia", "Zulma", "Zümra", "Zuzana", "Zuzu",
        ]
        
        self.nationality = [
            "Japanese", "French", "Russian", "Chinese", "Italian",
            "Arabic", "Spanish", "English", "German", "Korean",
            "Australian", "American", "Canadian", "Scotish",
            "Irish", "Welsh", "Polish", "Greek"
        ]

        # Eye colors has Golden Yellow instead of Golden Blonde
        self.eye_base_colors = [c if c != "Golden Blonde" else "Golden Yellow" for c in self.base_colors]

        self.skin_colors = [
            "Ivory White Pale", "Peach Fair", "Dark Bronze Brown", 
            "Dark Chocolate Brown", "Very Dark Ebony Black"
        ]

        self.body_types = ["Skinny", "Slim", "Regular", "Athletic", "Curvy"]
        
        self.hair_lengths = [
            "short ear-length", "medium chin-length", "medium neck-length", 
            "medium shoulder-length", "long back-length", "very-long hip-length", 
            "very-long thigh-length", "very-long knee-length", "very-long foot-length"
        ]

        self.personality = [
            "Adventurous", "Athletic", "Tsundere", "Bossy", "Motherly", "Nerdy", "Go-Getter",
            "Flirtatious", "Insecure", "Innocent", "Obedient", "Perfectionist", "Shy", "Bubbly",
            "Stoic", "Friendly", "Peaceful", "Wild", "Ambitious", "Independent", "Empathic"
        ]

        is_nsfw = self.is_nsfw.get()
        
        if is_nsfw:
            self.location = ["On the bed", "At a swimming pool", "At the beach", "At a water park"]
        else:
            self.location = ["At a swimming pool", "At the beach", "At a water park"]

        self.birthmonth = [
            "January", "February", "March", "April", "May", "June", "July",
            "August", "September", "October", "November", "December"
        ]

    def get_birthday(self, month):
        if month == "January":
            birthday = random.randint(1, 31)
        elif month == "March":
            birthday = random.randint(1, 31)
        elif month == "April":
            birthday = random.randint(1, 30)
        elif month == "May":
            birthday = random.randint(1, 31)
        elif month == "June":
            birthday = random.randint(1, 30)
        elif month == "July":
            birthday = random.randint(1, 31)
        elif month == "August":
            birthday = random.randint(1, 31)
        elif month == "September":
            birthday = random.randint(1, 30)
        elif month == "October":
            birthday = random.randint(1, 31)
        elif month == "November":
            birthday = random.randint(1, 30)
        elif month == "December":
            birthday = random.randint(1, 31)
        else:
            birthday = random.randint(1, 29)

        return birthday

    def get_hair_color(self):
        return random.choice(self.base_colors)

    def get_eye_color(self):
        if random.random() < 0.2: # 20% chance for heterochromia
            colors = random.sample(self.eye_base_colors, 2)
            return f"Heterochromia (Left: {colors[0]}, Right: {colors[1]})"
        return random.choice(self.eye_base_colors)

        try:
            response = requests.get(url, headers=headers, timeout=3)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # The Bump uses specific classes for names and origins, approximating here:
                name_tags = soup.find_all('div', class_='name-link') 
                if name_tags:
                    choice = random.choice(name_tags).text.strip()
                    return choice, "Mixed/Parsed"
        except Exception:
            pass 
        
        # Fallback if parsing fails or layout changes
        return random.choice(fallback_data)

    def get_swimsuit_color(self):
        swimsuit_color = random.choice(self.eye_base_colors)

    def scrape_hairstyle(self):
        """Attempts to scrape Fandom. Falls back to a hardcoded list if blocked."""
        url = "https://ideas.fandom.com/wiki/List_of_hairstyles"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        fallbacks = [
            "Bob cut", "Ponytail", "Twintails", "Tri-tails", "Messy bun", "Pixie cut", 
            "French braid", "Hime cut", "Drill hair", "Straight down", "Wavy hair",
            "Spiky hair", "Afro", "Natural", "Blunt cut", "Bowl cut", "Butch cut",
            "Asymmetric cut", "Chignon", "Dice bob", "Crown braid", "Emo mullet",
            "Fishtail braid", "Flipped hair", "Half-updo", "Layered hair", "Liberty spikes",
            "Afro Puffs", "Parted hair", "Pigtails", "Queue hair", "Rattail", "Ringlets",
            "Slicked-back hair", "Surfer hair"
        ]

        try:
            response = requests.get(url, headers=headers, timeout=3)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                items = soup.find_all('li')
                styles = [item.text.split('\n')[0].strip() for item in items if len(item.text) > 3 and len(item.text) < 30]
                if styles:
                    return random.choice(styles)
        except Exception:
            pass

        return random.choice(fallbacks)

    def get_age_and_height(self):
        is_nsfw = self.is_nsfw.get()
        
        if is_nsfw:
            age = random.randint(18, 25)
        else:
            age = random.randint(6, 25)
        
        if age <= 12:
            age_category = "child"
        elif age <= 17 and age >= 13:
            age_category = "teenager"
        else:
            age_category = "adult"

        # Height Logic (in inches)
        if age >= 18:
            height_inches = random.randint(59, 84) # 4'11" to 7'0"
        else:
            # WHO Growth Chart approximations for girls (5th to 95th percentiles)
            who_data = {
                6: (43, 49), 7: (45, 51), 8: (47, 54), 9: (49, 56), 10: (51, 59),
                11: (53, 62), 12: (56, 64), 13: (58, 66), 14: (59, 67), 
                15: (60, 68), 16: (60, 68), 17: (60, 68)
            }
            min_in, max_in = who_data.get(age, (43, 68))
            height_inches = random.randint(min_in, max_in)

        # Convert to feet/inches
        feet = height_inches // 12
        inches = height_inches % 12
        height_str = f"{feet}'{inches}\""

        # Categorize
        if height_inches <= 64:
            category = "Petite"
        elif 65 <= height_inches <= 67:
            category = "Regular"
        else:
            category = "Tall"

        return age, height_str, category, age_category

    def get_brightness(self, skin):
        if self.skin_colors == "Dark Bronze Brown" or "Dark Chocolate Brown" or "Very Dark Ebony Black":
            brightness = "dark"
        elif self.skin_colors == "Peach Fair":
            brightness = "fair"
        elif self.skin_colors == "Ivory White Pale":
            brightness = "pale"
        else:
            brightness = "null"

        return brightness

    def get_zodiac_sign(self, month, day):
        if (month == "March" and day >= 20) or (month == "April" and day <= 19): 
            zodiac_sign = "🐏 Aries"
        elif (month == "April" and day >= 20) or (month == "May" and day <= 20): 
            zodiac_sign = "🐂 Taurus"
        elif (month == "May" and day >= 21) or (month == "June" and day <= 20): 
            zodiac_sign = "🧑‍🤝‍🧑 Gemini"
        elif (month == "June" and day >= 21) or (month == "July" and day <= 22): 
            zodiac_sign = "🦀 Cancer"
        elif (month == "July" and day >= 23) or (month == "August" and day <= 22): 
            zodiac_sign = "🦁 Leo"
        elif (month == "August" and day >= 23) or (month == "September" and day <= 22): 
            zodiac_sign = "👩🏻 Virgo"
        elif (month == "September" and day >= 23) or (month == "October" and day <= 22): 
            zodiac_sign = "⚖️ Libra"
        elif (month == "October" and day >= 23) or (month == "November" and day <= 21): 
            zodiac_sign = "🦂 Scorpio"
        elif (month == "November" and day >= 22) or (month == "December" and day <= 21): 
            zodiac_sign = "🏹 Sagittarius"
        elif (month == "December" and day >= 22) or (month == "January" and day <= 19): 
            zodiac_sign = "🐐 Capricorn"
        elif (month == "January" and day >= 20) or (month == "February" and day <= 17): 
            zodiac_sign = "🫗 Aquarius"
        elif (month == "February" and day >= 18) or (month == "March" and day <= 19): 
            zodiac_sign = "🐟 Pisces"
        else:
            zodiac_sign = "[?] Unknown"

        return zodiac_sign

    def generate(self):
        self.log_area.delete(1.0, tk.END) # Clear log
        
        # Gather Data
        age, height_val, height_cat, age_cat = self.get_age_and_height()
        name = random.choice(self.names)
        month = random.choice(self.birthmonth)
        birthday = self.get_birthday(month)
        zodiac_sign = self.get_zodiac_sign(month, birthday)
        nationality = random.choice(self.nationality)
        personality = random.choice(self.personality)
        swimsuit_color = random.choice(self.eye_base_colors)
        hairstyle = self.scrape_hairstyle()
        chest = random.choice(self.chest_sizes)
        hair_color = self.get_hair_color()
        eye_color = self.get_eye_color()
        skin = random.choice(self.skin_colors)
        brightness = self.get_brightness(skin)
        body = random.choice(self.body_types)
        hair_length = random.choice(self.hair_lengths)
        location = random.choice(self.location)
        seed = random.randint(1, 4294967295)
        is_nsfw = self.is_nsfw.get()

        # Build Profile Text
        profile = f"--- CHARACTER PROFILE ---\n"
        profile += f"Name: {name}\n"
        profile += f"Nationality: {nationality}\n"
        profile += f"Age: {age} year old " + f"{age_cat}\n"
        profile += f"Species: Human\n"
        profile += f"Birthday: {month} {birthday}\n"
        profile += f"Zodiac Sign: " + f"{zodiac_sign}\n"
        profile += f"Personality: {personality}\n"
        profile += f"Height: {height_val} [{height_cat}]\n"
        profile += f"Body Type: {body}\n"
        profile += f"Chest Size: {chest}\n"
        profile += f"Skin Tone: {skin} skin\n"
        profile += f"Hair: {hair_color}, {hair_length}, {hairstyle}\n"
        profile += f"Eyes: {eye_color}\n"
        profile += f"Outfit: Two-toned {swimsuit_color} One-piece racerback competition swimsuit\n"
        profile += f"Location: {location}\n\n"

        # Build Open-Source AI Image Prompt (Stable Diffusion / Danbooru format)
        prompt_tags = [
            f"(" + "masterpiece", "professionally best quality", "perfect eyes", "accurate proportions", "perfect anatomy",
            "perfect 4-fingered hands" , "random expression", f"{{full body|cowboy shot|upper body|portrait|close-up|feet out of frame}}",
            f"visual novel:1.3)", "1girl", "solo", f"{age}yo " + f"(({age_cat}))", f"{body} body", chest.replace("_", " "),
            f"{skin}" + " skin", f"{brightness}-skinned female", "an " f"{personality} {height_cat} {nationality} human girl named {name}",
            f"{hair_color} {hair_length} hair", f"{hairstyle}",
            eye_color.replace("Heterochromia (Left: ", "heterochromia, ").replace(", Right:", " and").replace(")", "") + " eyes",
            "two-toned " + f"{swimsuit_color}" + " one-piece racerback competition swimsuit", "skintight swimsuit", f"{location}",
            f"(accurate location, accurate skin tone, accurate hair, accurate eyes, " + f"{{looking at viewer|looking away}}",
            f"{{front view|back view|side view|top view|bottom view}}, character consistency:1.4)"
        ]

        if is_nsfw:
            prompt_tags.extend(["nsfw", "explicit"])
        else:
            # SFW tags enforced as requested for default state
            prompt_tags.extend(["sfw", "safe", "rating:general"])

        avoid_tags = [
            f"(" + "blurry", "pixelated", "low quality", "bad anatomy", "distorted face", "asymmetrical features", "unnatural skin tones",
            "incorrect proportions", "extra limbs", "deformed hands", "missing fingers", "poorly rendered eyes", "unnatural shadows",
            "overexposed", "underexposed", "dull colors", "low contrast", "grainy", "watermark", "signature", "text", "logo", "broken art",
            "glitchy mess", "completely unrelated", "cropped", "zoomed", "normal quality", "cameltoe", "nipples", "simple background", "realistic",
            "photorealistic" + f", monotone swimsuit, three-toned hair:1.5)"
        ]

        if is_nsfw:
            avoid_tags.extend([""])
        else:
            # SFW tags enforced as requested for default state
            avoid_tags.extend(["nsfw", "explicit"])

        ai_prompt = ", ".join(prompt_tags)
        nega_prompt = ", ".join(avoid_tags)

        profile += f"--- AI IMAGE PROMPT (Goes in Description Box) ---\n{ai_prompt}\n\n"
        profile += f"--- Seed: {seed} ---\n\n"
        profile += f"--- NEGATIVE PROMPT (Goes in Anti-Description Box) ---\n{nega_prompt}\n\n"
        profile += "*(Copy and paste the above prompts into Automatic1111, ComfyUI, or your preferred open-source model)*\n\n"
        profile += "Now have fun generating with your image prompt and negative prompt!\n\n"

        self.log_area.insert(tk.END, profile)

if __name__ == "__main__":
    root = tk.Tk()
    app = CharacterGenerator(root)
    root.mainloop()
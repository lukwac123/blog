# Aplikacja Blog zbudowana z użyciem framework'a Django.

Przedstawiony projekt bloga zbudowany został z głównych komponentów Django służacych do tworzenia modeli danych, systemu szablonów, a także obsługi formularzy i autoryzacji użytkowników. Dzięki temu możliwe jest dodawanie, edytowanie i zarządzanie postami przez administratora, a także komentowanie treści przez użytkowników. Projekt podzielony został na etapy, począwszy od konfiguracji środowiska, przez tworzenie bazy danych, aż po implementację funkcji publikacji. Ważnym elementem będzie również system uwierzytelniania, który pozwoli na zabezpieczenie dostępu do części administracyjnej aplikacji. Projekt bloga pokaże, jak w praktyce używać ORM Django do zarządzania bazą danych oraz jak korzystać z frameworka do obsługi widoków i routingu URL.

![Screenshot from 2024-10-18 10-52-41](https://github.com/user-attachments/assets/1a69bab3-0b9c-4607-8791-49b399fbc837)
<sup>Rys. Strona główna aplikacji Blog</sup>

## Przebieg projektu:
1. Tworzenie środowiska wirtualnego w Pythonie.
2. Instalacja Django.
3. Utworzenie projektu Django.
4. Utworzenie aplikacji Django.
5. Projektowanie modeli danych.
6. Tworzenie witryny administracyjnej dla modeli.
7. Przygotowanie widoków listy i szczegółów.
8. Utworzenie szablonów dla widoków.
9. Usprawnienie i rozbudowa aplikacji.

## 1. Tworzenie środowiska wirtualnego w Pythonie.

Środowisko wirtualne w Pythonie to izolowany zestaw narzędzi, który pozwala na instalację specyficznych wersji pakietów i bibliotek, niezależnych od globalnych instalacji Pythona na komputerze. Dzięki temu można uniknąć konfliktów między wersjami pakietów w różnych projektach. Środowiska te są szczególnie przydatne przy pracy nad wieloma projektami jednocześnie, ponieważ pozwalają na utrzymanie odpowiednich zależności. Korzystanie ze środowisk wirtualnych jest standardową praktyką w projektach Pythonowych, ponieważ zapewnia kontrolę nad wersjami bibliotek i minimalizuje ryzyko problemów przy wdrażaniu aplikacji.

W projekcie środowisko wirtualne zostało wykonane za pomocą polecenia:
```
python3 -m venv blog_env
```
Powyższe polecenie tworzy wspomiane środowisko witrualne w tym przypadku w folderze _blog_env/_
Korzystając z systemu Linux aktywacja środowiska następuje po wpisaniu polecenia:
```
source blog_env/bin/activate
```
Symbol zachęty zawiera ujątą w nawiasy nazwę aktywnego śrdodowiska wirtualnego np.:
```
(blog_env) lukasz@lukasz-ThinkPad-T560:~
```
Za pomocą polecenia *deactivate* można w dowolnym momencie zdezaktywować środowisko.

## 2. Instalacja Django.

Instalacji Django dokonujemy będąc w folderze z aktywnym środowiskiem wirtualnym utworzonym w poprzednim punkcie przy użyciu instalatora pakietów *pip*
```
pip install Django
```
Polecenie to zainstaluje najnowszą dostępną wersję.

### 2.1 Główne komponenty frameworka.

Django to framework do tworzenia aplikacji internetowych w Pythonie, który upraszcza proces budowania aplikacji, oferując wiele wbudowanych narzędzi i funkcji. Jego struktura opiera się na architekturze Model-View-Template (MVT), co ułatwia podział aplikacji na trzy główne komponenty:
+ *model* - dpowiada za definiowanie struktury danych oraz interakcje z bazą danych, zapewniając wygodną abstrakcję nad warstwą danych.
+ *szablon* - to komponent odpowiadający za generowanie HTML, który łączy dane dynamiczne z warstwą prezentacji.
+ *widok* - odpowiada za logikę aplikacji, przetwarzając żądania użytkowników i zwracając odpowiednie odpowiedzi w formie zrenderowanych stron lub innych danych.

### 2.2 Architektura Django.

Sposób przetwarzania żądań oraz zarządzanie cyklem żądanie-odpowiedź:

![Django-2024-10-18-081610](https://github.com/user-attachments/assets/9857b0fc-52c8-4148-9ed0-73fe7a9d10d7)
<sup>Rys. Architektura Django.</sup>

1. Przeglądarka: Użytkownik wysyła żądanie HTTP (np. klikając link lub wprowadzając adres URL).
2. URL: Django dopasowuje żądany URL do odpowiedniego widoku na podstawie zdefiniowanych wzorców URL.
3. Widok: Widok pobiera odpowiednie dane (logika aplikacji) lub modyfikuje je, współpracując z modelem.
4. Model: Jeśli potrzebne są dane, model komunikuje się z bazą danych w celu pobrania lub zapisania danych.
5. Baza danych: Odpowiada na zapytanie modelu, zwracając żądane dane.
6. Widok: Otrzymane dane są przetwarzane i przekazywane do szablonu w celu wygenerowania strony.
7. Szablon: Szablon renderuje dynamiczne dane do formatu HTML.
8. Widok: Zwraca wygenerowaną stronę HTML.
9. Przeglądarka: Ostatecznie użytkownik widzi wygenerowaną stronę w przeglądarce.

## 3. Utworzenie i konfiguracja projektu Django

Django zawiera polecenie, które utworzy początkową strukture plików projektu. Znajdujemy się w głównym katalogu _blog_ który jest kontenerem dla tego projektu. 
Będąc w tym folderze wpisujemy polecenie:
```
django-admin startproject blog_project
```
Spowoduje to utworzenie projektu Django o nazwie *blog_project*

Powstała struktura plików powinna wyglądać następująco:
```
blog/
    manage.py
    blog_project/
        __init__.py
        asgi.py
        settings.py
        urls.py
        wsgi.py
```
### 3.1 Pierwsza migracja bazy danych.

Ponieważ Django do przechowywania danych używa bazy danych, domyślnie jest to SQLite3. Na początek należy utworzyć tabele dla początkowych aplikacji,
które domyślnie są załączone w pliku _settings.py_ należącego do projektu. Będąc w folderze głównym _blog/_ dokonujemy tego porzez wpisanie polecenia:
```
python3 manage.py migrate
```
Aby sprawdzać wprowadzone zmiany należy uruchomić serwer programistyczny, który uruchamia się poleceniem:
```
python3 manage.py runserver
```
Następnie z konsoli klikamy na wyświetlony link _http://127.0.0.1:8000/_ i powinniśmy zobaczyć ekran powitalny z informacją:"Instalacja przebiegła pomyślnie! Gratulacje!"

## 4. Utworzenie aplikacji.

Będąc w katalogu głównym projektu _blog/_ należy wpisać poniższe polecenie:
```
python3 manage.py startapp blog
```
Spowoduje to utworzenie podstawowej struktury aplikacji, która powinna wyglądać następująco:
```
blog/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```

# 5. Projektowanie modeli danych.

Model Django jest źródłem informacji i sposobu w jaki mają zachowowywać się dane. Składa się on z klasy Pythona, która jest podklasą klasy **django.db.models.Model**.
Każdy model można zmapować na pojedyńczą tabelę bazy danych, a każdy atrybut tej klasy reprezentuje pole bazy danych. Modele tworzymy w pliku **models.py** w floderze aplikacji _blog/_.
Dla przykładu poniżej przedstawiony został model **Post**:
```
class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Roboczy'
        PUBLISHED = 'PB', 'Opublikowany'
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    
    object = models.Manager() # Menedżer domyślny.
    published = PublishedManager() # Menedżer niestandardowy.

    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish']),]


    def __str__(self):
        return self.title
    

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])

    tags = TaggableManager()
```
Dla powyższego modelu zdefiniowane zostały następujące pola:

+ **title** - pole reprezentujące tytuł posta. Jest to pole tylu CharField, które w bazie danych SQL odpowiada kolumnie VARCHAR.
+ **slug** - jest to krótka etykiet zawierająca wyłącznie litery, cyfry, znaki podkreślenia lub łączniki. W projekcie posłużyła do tworzenia
przyjaznych dla SEO adresów URL.
+ **body** - pole zawierające treść postu. Jest to pole typu TextField, które w bazie danych SQL odpowiada kolumnie TEXT.
+ **author** - pole to definiuje relację wiele do jednego. Daje to informację, że każdy post jest napisany przez określonego użytkownika. Za 
jego pomocą Django utworzy klucz obcy w bazie danych z wykorzystaniem klucza głównego powiązanego modelu.
+ **publish** - pole typu DataTimeField co w bazie danych odpowiada kolumnie DATATIME. Pole przechowuje datę i godzinę opublikowania posta.
+ **created** - jak powyżej, przechowuje datę i godzinę utworzenia posta.
+ **updated** - jak powyżej, przecowuje datę i godzinę aktualizacji posta.

Klasa **Status** dodaje pole, które określa stan posta, domyślnie ustawiona została jako "wersja robocza" która w blogu nie jest widoczna dla uzytkowników.
Dopiero zmiana statusu na "opublikowany" udostępnia post dla pozostałych uzytkowników.

Klasa **Meta** służy do sortowania wyników według pola **publish**, dodanie znaku "-" powoduje że wyświetlamy wyniki w kolejności malejącej.

Metoda **__str__** jest domyślną metodą Pythona która zwraca ciąg znaków.

Metoda **get_absolute_url_** zawiera funkcję **reverse()** która zbuduje adres URL dynamicznie, z wykorzystaniem nazwy adresu URL zdefiniowanych we wzorcach adresów URL.

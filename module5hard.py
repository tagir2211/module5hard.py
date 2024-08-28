class user:
    '''
    Каждый объект класса User должен обладать следующими атрибутами и методами:
    Атриубуты:  nickname(имя пользователя, строка),
                password(в хэшированном виде, число),
                age(возраст, число)
    '''
    u_data = []
    u_keys = ['login', 'password', 'age']
    def __new__(cls, *args):
        cls.u_data.append(dict(zip(cls.u_keys, args)))
        return super().__new__(cls)
    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = password
        self.age = age

class Video:
    '''
    Каждый объект класса Video должен обладать следующими атрибутами и методами:
    Атриубуты:  title(заголовок, строка),
                duration(продолжительность, секунды),
                time_now(секунда остановки (изначально 0)),
                adult_mode(ограничение по возрасту, bool (False по умолчанию))
    '''
    v_data = []
    title_data = []
    v_keys = ['title', 'duration', 'time_now', 'adult_mode']
    def __init__(self, title, duration, time_now = 0, adult_mode = False):
        self.title = title
        self.duration = duration
        self.time_now = time_now
        self.adult_mode = adult_mode
        self.v_data.append(dict(zip(self.v_keys, [title, duration, time_now, adult_mode])))
        self.title_data.append(title)


class UrTube:
    '''
     Каждый объект класса UrTube должен обладать следующими атрибутами и методами:
     Атриубты:  users(список объектов User),
                videos(список объектов Video),
                current_user(текущий пользователь, User)
   '''
    def __init__(self):
        self.users = user
        self.videos = Video
        self.current_user = None


    def log_in(self, nickname, password):
        '''
        Метод log_in, который принимает на вход аргументы: nickname, password
        и пытается найти пользователя в users с такими же логином и паролем.
        Если такой пользователь существует, то current_user меняется на найденного.
        Помните, что password передаётся в виде строки, а сравнивается по хэшу.
        '''
        for i in self.users.u_data:
            if i.get('login') == nickname and hash(i.get('password')) == hash(password):
                self.current_user = i.get('login')
                print('Вы вошли в систему под логином - ', nickname)

    def register(self, nickname, password, age):
        '''
        Метод register, который принимает три аргумента:
        nickname, password, age,
        и добавляет пользователя в список, если пользователя не существует (с таким же nickname).
        Если существует, выводит на экран: "Пользователь {nickname} уже существует".
        После регистрации, вход выполняется автоматически.
      '''

        if self.users.u_data != []:
            for i in self.users.u_data:
                if i.get('login') == nickname:
                    print(f"Пользователь {nickname} уже существует.")
                    break
                else:
                    new_user = dict(zip(self.users.u_keys, [nickname, password, age]))
                    self.users.u_data.append(new_user)
                    self.current_user = nickname
                    self.log_in(nickname, password)
                    break
        else:
            new_user = dict(zip(['login', 'password', 'age'], [nickname, hash(password), age]))
            self.users.u_data.append(new_user)
            self.current_user = nickname
            self.log_in(nickname, password)


    def log_out(self):
        '''
        Метод log_out для сброса текущего пользователя на None.
        '''
        self.current_user = None
    def add(self, *args):
        '''
        Метод add, который принимает неограниченное кол-во объектов класса Video
        и все добавляет в videos, если с таким же названием видео ещё не существует.
        В противном случае ничего не происходит.
        '''

        for i in args:
            if i.title in self.videos.title_data:
                break
            else:
                self.videos.v_data.append(dict(zip(self.videos.v_keys, i)))
    def get_videos(self, search_str):
        '''
      Метод get_videos, который принимает поисковое слово и
      возвращает список названий всех видео, содержащих поисковое слово.
      Следует учесть, что слово 'UrbaN' присутствует в строке 'Urban the best' (не учитывать регистр).
      '''
        search_resalt = []
        for i in self.videos.title_data:
            if search_str.lower() in i.lower():
                search_resalt.append(i)
        return f'Результаты поиска по слову -  {search_str} : {search_resalt}'

    def watch_video(self, name_video):
        '''
      Метод watch_video, который принимает название фильма,
      если не находит точного совпадения(вплоть до пробела),
      то ничего не воспроизводится, если же находит - ведётся отчёт в консоль
      на какой секунде ведётся просмотр. После текущее время просмотра данного видео сбрасывается.
        '''
        cur_user_ind = None
        for i in self.users.u_data:
            if i.get('login') == self.current_user:
                cur_user_ind = self.users.u_data.index(i)
            else:
                continue
        vidio_index = None
        for i in self.videos.v_data:
            if i.get('title') == name_video:
                vidio_index = self.videos.v_data.index(i)
            else:
                continue
        if vidio_index == None:
            print(f'даное видео не найдено')
        elif cur_user_ind == None:
            print(f'Для простомтра видео необходимо войти в систему')
        else:
            if self.users.u_data[cur_user_ind].get('age') >= 18 or not self.videos.v_data[vidio_index].get('adult_mode'):
                from time import sleep
                for i in self.videos.v_data:
                    if i.get('title') == name_video:
                        print(f'Просмотр видео: {name_video}')
                        t = 0
                        for j in range(i.get('duration')):
                            t = i.get('time_now') + 1
                            i.update({'time_now': t})
                            print(i.get('time_now'), end=' ')
                            sleep(1)
                            if i.get('time_now') == i.get('duration'):
                                i.update({'time_now': 0})
                        print('Конец видео')
                        break
                else:
                    return f'Видео {name_video} не найдено'
            else:
                print(f'Видео недоступно для {self.current_user}')


ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)

ur.watch_video('Для чего девушкам парень программист?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')

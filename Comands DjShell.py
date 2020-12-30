# пользователи
User.objects.create(username='Bob', password='123')
User.objects.create(username='Brian', password='qwerty')

# авторы (в модели уже пользователи поэтому id 1 и 2)
Author.objects.create(author=User.objects.get(id=1))
Author.objects.create(author=User.objects.get(id=2))

# категории
Category.objects.create(name='Политика')
Category.objects.create(name='История')
Category.objects.create(name='Космос')
Category.objects.create(name='Финансы')

# новости и статьи
# Повторить в зависимости от желаемого количества новостей
Post.objects.create(author=Author.objects.get(id=1), type = 'NW',
                    header= 'Еще одна интересная новость',
                    article_text='Прикольный текст, который используется в новости')

# Присваиваем категории новости из примера выше id=1
post = Post.objects.get(id=1)
post.category.add(Category.objects.get(id=1))

# комментарии
author = User.objects.get(id=2)
post = Post.objects.get(id=1)
Comment.objects.create(post=post, author=author, text='текст комментария')

# лайки комментариям
comments = Comment.objects.all()
comments[0].like() # один лайк для Brian

# лайки для поста
post.like()

# меняем рейтинг посту
post.post_raiting = 100
post.save()

# обновляем рейтинги авторов
for auth in Author.objects.all():
    auth.update_raiting()

# выводим имя и рейтинг лучшего пользоветеля
Author.objects.all().order_by('-author_raiting').values('author__username','author_raiting')[0]

# выводим лучшую статью
best = Post.objects.all().order_by('-post_raiting')[0]
best_post= Post.objects.all().order_by('-post_raiting').values( # выводим параметры
    'created_time',
    'author__author__username',
    'header', 'post_raiting',
    'article_text')[0]
best.preview()

# выводим все комментарии к статье
Comment.objects.filter(post=best).values('author__username', 'created_time', 'text')
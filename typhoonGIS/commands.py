import click
from tyhoonGIS import db,app
from models import  User,Typhoon
@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()
    data = pd.read_csv(r"F:\Desktop\和鲸项目\WebGIS\typhoon\typhoon\typhoon2022.csv")
    Typhoons = data[['name', 'ename', 'begin_time', 'end_time']].drop_duplicates()
    fields = Typhoons.columns.tolist()
    Typhoons['begin_time'] = pd.to_datetime(Typhoons['begin_time'])
    Typhoons['end_time'] = pd.to_datetime(Typhoons['end_time'])
    Typhoons = Typhoons.to_dict(orient='records')

    for t in Typhoons:
        t= Typhoon(name=t['name'], ename=t['ename'], begin_time=t['begin_time'], end_time=t['end_time'])
        db.session.add(t)
    db.session.commit()
    click.echo('Done.')



@app.cli.command()  # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息

@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)  # 设置密码
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)  # 设置密码
        db.session.add(user)

    db.session.commit()  # 提交数据库会话
    click.echo('Done.')


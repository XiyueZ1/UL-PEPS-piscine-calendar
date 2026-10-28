# PEPS piscine → Google Calendar

[Français](#français) · [English](#english) · [中文](#中文)

---

<a name="français"></a>
## Français

Convertit l'horaire des [bains libres](https://peps.ulaval.ca/activite/bains-libres) du PEPS de l'Université Laval en fichier `.ics`, à importer dans Google Agenda, Apple Calendrier ou Outlook.

### Fonctionnalités

* Récupère automatiquement l'horaire des deux prochaines semaines sur le site officiel
* Filtre par type de bain, par piscine et par longueur de couloir
* Chaque événement indique la piscine, la longueur, la profondeur et les notes du site (par exemple, 3 couloirs seulement à certaines heures)
* Chaque plage horaire a un identifiant fixe. Importer deux fois dans le même agenda ne crée pas de doublon.
* Les événements sont marqués « disponible » et ne bloquent pas votre agenda
* Fonctionne sur Mac et Windows

### Installation

Python 3.8 ou plus récent est requis.

```
git clone https://github.com/XiyueZ1/UL-PEPS-piscine-calendar.git
cd UL-PEPS-piscine-calendar
pip install -r requirements.txt
```

Sur Mac, remplacez `pip` par `python3 -m pip`. Sur Windows, utilisez `py -m pip` ou `python -m pip`.

### Utilisation

```
python peps_piscine.py
```

Un fichier `.ics` est créé dans le dossier courant. Son nom contient les dates, par exemple `peps_piscine_1004-1018.ics`.

Vous pouvez aussi double-cliquer sur `run_piscine.command` (Mac) ou `run_piscine.bat` (Windows). Le dossier s'ouvre automatiquement à la fin.

#### Options

| Option | Effet |
|---|---|
| (aucune) | Bains 13 ans et plus, toutes les piscines |
| `--type tous` | Bains pour tous seulement |
| `--type all` | Les deux types de bains |
| `--pool olympique` | Piscine olympique seulement |
| `--pool tremplins` | Piscine avec tremplins seulement |
| `--min-length 25` | Couloirs de 25 m ou plus |
| `--length 21` | Couloirs de 21 m exactement |
| `--shallow` | Plages avec eau peu profonde |
| `--file page.html` | Lit une page enregistrée depuis le navigateur, sans connexion |
| `--out nom.ics` | Nom du fichier de sortie |

Les options peuvent être combinées :

```
python peps_piscine.py --pool olympique --min-length 50
```

### Importer dans Google Agenda

L'importation se fait dans la version Web, sur ordinateur. L'application mobile ne le permet pas.

1. Créez d'abord un agenda séparé : à côté de « Autres agendas », cliquez sur **+**, puis « Créer un agenda ». Nommez-le par exemple `PEPS piscine`.
2. Ouvrez **Paramètres**, puis **Importer et exporter**. Choisissez le fichier `.ics`, sélectionnez l'agenda créé, puis cliquez sur **Importer**.

Le site publie l'horaire deux semaines à l'avance. Lancez le programme environ toutes les deux semaines. Importez toujours dans le même agenda pour éviter les doublons.

Si le PEPS modifie l'heure d'une plage, l'ancien événement n'est pas supprimé. Pour garder un agenda exact, supprimez et recréez l'agenda avant chaque importation.

### Questions fréquentes

**Erreur de certificat SSL**
Un RPV, un antivirus ou le réseau de l'université remplace parfois le certificat HTTPS. Le programme essaie alors le curl du système, puis ignore la vérification du certificat en dernier recours. La page est publique et ne contient aucune donnée de compte.

**Message « 没找到课表 » (horaire introuvable)**
Le site a peut-être changé. Enregistrez la page en `.html` depuis le navigateur et relancez avec `--file`. Si le problème persiste, les mots-clés de `parse()` doivent être mis à jour. N'hésitez pas à ouvrir une issue.

### Tests

```
python -m unittest discover -s tests -v
```

### Avis

Projet personnel, sans lien avec l'Université Laval ni le PEPS. Vérifiez toujours l'[horaire officiel](https://peps.ulaval.ca/activite/bains-libres) avant de vous déplacer.

Code écrit avec l'aide de Claude (Anthropic).

### Licence

[MIT](LICENSE)

---

<a name="english"></a>
## English

Converts the [free swim schedule](https://peps.ulaval.ca/activite/bains-libres) of the PEPS sports centre at Université Laval into an `.ics` file you can import into Google Calendar, Apple Calendar or Outlook.

### Features

* Fetches the next two weeks of the schedule from the official website
* Filters by swim type, pool and lane length
* Each event shows the pool, lane length, water depth and the notes from the website (for example, only 3 lanes at certain times)
* Each time slot has a fixed ID. Importing it twice into the same calendar does not create a duplicate.
* Events are marked "free", so they do not block your calendar
* Works on Mac and Windows

### Installation

Requires Python 3.8 or later.

```
git clone https://github.com/XiyueZ1/UL-PEPS-piscine-calendar.git
cd UL-PEPS-piscine-calendar
pip install -r requirements.txt
```

On Mac, replace `pip` with `python3 -m pip`. On Windows, use `py -m pip` or `python -m pip`.

### Usage

```
python peps_piscine.py
```

An `.ics` file is created in the current folder. Its name includes the date range, for example `peps_piscine_1004-1018.ics`.

You can also double-click `run_piscine.command` (Mac) or `run_piscine.bat` (Windows). The folder opens automatically when it is done.

#### Options

| Option | Effect |
|---|---|
| (none) | Lap swims (13 and over), all pools |
| `--type tous` | Family swims only |
| `--type all` | Both swim types |
| `--pool olympique` | Olympic pool only |
| `--pool tremplins` | Diving pool only |
| `--min-length 25` | Lanes of 25 m or longer |
| `--length 21` | Lanes of exactly 21 m |
| `--shallow` | Slots with shallow water |
| `--file page.html` | Reads a page saved from your browser, no internet needed |
| `--out name.ics` | Output file name |

Options can be combined:

```
python peps_piscine.py --pool olympique --min-length 50
```

### Import into Google Calendar

Use the web version on a computer. The mobile app cannot import files.

1. First create a separate calendar: next to "Other calendars", click **+**, then "Create new calendar". Name it something like `PEPS piscine`.
2. Open **Settings**, then **Import & export**. Choose the `.ics` file, select the calendar you created, then click **Import**.

The website publishes the schedule two weeks ahead. Run the program about every two weeks. Always import into the same calendar to avoid duplicates.

If PEPS changes the time of a slot, the old event is not removed. To keep the calendar exact, delete and recreate the calendar before each import.

### FAQ

**SSL certificate error**
A VPN, antivirus or the university network sometimes replaces the HTTPS certificate. The program then tries the system's curl, and skips certificate verification as a last resort. The page is public and contains no account data.

**Message "没找到课表" (schedule not found)**
The website may have changed. Save the page as `.html` from your browser and run again with `--file`. If that does not work, the keywords in `parse()` need updating. Feel free to open an issue.

### Tests

```
python -m unittest discover -s tests -v
```

### Disclaimer

Personal project, not affiliated with Université Laval or PEPS. Always check the [official schedule](https://peps.ulaval.ca/activite/bains-libres) before you go.

Written with the help of Claude (Anthropic).

### Licence

[MIT](LICENSE)

---

<a name="中文"></a>
## 中文

将PEPS游泳池开放时间表（[Bains libres](https://peps.ulaval.ca/activite/bains-libres)）转换成 `.ics` 日历文件，可导入 Google 日历、Apple 日历或 Outlook。

### 功能

* 自动抓取官网最新两周的时间表
* 可以按场次、泳池和泳道长度筛选
* 每个事件包含泳池、泳道长度、水深和备注
* 每个时段有固定编号，重复导入同一个日历时不会出现两份
* 事件设为“空闲”，不会让你的日历显示忙碌
* 支持 Mac 和 Windows

### 安装

需要 Python 3.8 或更新的版本。

```
git clone https://github.com/XiyueZ1/UL-PEPS-piscine-calendar.git
cd UL-PEPS-piscine-calendar
pip install -r requirements.txt
```

Mac 上把 `pip` 换成 `python3 -m pip`。Windows 上换成 `py -m pip` 或 `python -m pip`。

### 使用

```
python peps_piscine.py
```

运行后会在当前文件夹生成一个 `.ics` 文件，文件名带日期范围，比如 `peps_piscine_1004-1018.ics`。

也可以双击运行：Mac 用 `run_piscine.command`，Windows 用 `run_piscine.bat`。运行完会自动打开文件夹。

#### 选项

| 选项 | 作用 |
|---|---|
| （不加选项） | 所有泳池的 13 岁以上游泳场 |
| `--type tous` | 只要家庭场（Bains pour tous） |
| `--type all` | 两种场次都要 |
| `--pool olympique` | 只要奥林匹克池 |
| `--pool tremplins` | 只要跳水池 |
| `--min-length 25` | 只要 25 米及以上的泳道 |
| `--length 21` | 只要 21 米的泳道 |
| `--shallow` | 只要有浅水区的时段 |
| `--file 页面.html` | 读取浏览器另存的网页，不联网抓取 |
| `--out 文件名.ics` | 指定输出文件名 |

选项可以组合，比如：

```
python peps_piscine.py --pool olympique --min-length 50
```

### 导入 Google 日历

需要在电脑上的网页版操作，手机 app 不支持导入。

1. 建议先建一个单独的日历：左侧“其他日历”旁点 **+**，选“创建新日历”，取名比如 `PEPS piscine`。
2. 进入 **设置**，选 **导入和导出**，选择 `.ics` 文件，目标日历选刚建的那个，点 **导入**。

官网每次只公布未来两周，所以大约每两周运行一次。每次都导入同一个日历，就不会重复。

如果官网改了某个时段的时间，旧的事件不会自动删除。想保持日历完全准确，可以每次导入前删除并重建这个日历。

### 常见问题

**SSL 证书错误**
VPN、杀毒软件或学校网络有时会替换 HTTPS 证书。程序会自动改用系统自带的 curl，再不行就跳过证书验证。这只是一个公开的时间表页面，不涉及账号信息。

**提示“没找到课表”**
官网可能改版，可以在浏览器里把页面另存为 `.html`，用 `--file` 运行试试。如果还是不行，需要更新 `parse()` 里的关键词，欢迎提 issue。

### 运行测试

```
python -m unittest discover -s tests -v
```

### 说明

这是个人项目，与拉瓦尔大学和 PEPS 没有关联。时间表以 [PEPS 官网](https://peps.ulaval.ca/activite/bains-libres) 为准，出发前请再确认一下。

代码在 Claude（Anthropic）的协助下编写。

### 许可证

[MIT](LICENSE)

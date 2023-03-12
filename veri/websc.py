import requests
import pyodbc
from bs4 import BeautifulSoup

def get_soup(TARGET_URL):
    page = requests.get(TARGET_URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

page_urls = []
comp_urls = []

def get_page(site):
    if(site == "N11"):
        BASE_URL = 'https://www.n11.com/bilgisayar/dizustu-bilgisayar'
        page_urls.append(BASE_URL)
        soup = get_soup(BASE_URL)
        for i in range(0, 10):
            for k in soup.find_all('a', attrs={'class': 'next'}):
                page_urls.append(k['href'])
                soup = get_soup(k["href"])

        for link in page_urls:
            soup = get_soup(link)
            products = soup.find_all("li", attrs={'class': 'column'})
            for urun in products:
                comp_urls.append(urun.a.get("href"))
    elif(site == "TRENDYOL"):
        BASE_URL = 'https://www.trendyol.com/laptop-x-c103108?pi='
        for i in range(1, 5):
            sayfalink = BASE_URL + str(i)
            page_urls.append(sayfalink)
        url_start = "https://www.trendyol.com/"

        for link in page_urls:
            soup = get_soup(link)
            products = soup.find_all("div", attrs={'class': 'p-card-chldrn-cntnr card-border'})
            for urun in products:
                url_end = urun.a.get("href")
                url_total = url_start + url_end
                comp_urls.append(url_total)

    elif(site == "TEKNOSA"):
        BASE_URL = 'https://www.teknosa.com/laptop-notebook-c-116004?s=%3Arelevance&page='
        for i in range(0, 5):
            sayfalink = BASE_URL + str(i)
            page_urls.append(sayfalink)
        url_start = "https://www.teknosa.com"

        for link in page_urls:
            soup = get_soup(link)
            products = soup.find_all("div", attrs={'class': 'prd'})
            for urun in products:
                url_end = urun["data-product-url"]
                url_total = url_start + url_end
                comp_urls.append(url_total)

    elif(site == "HEPSIBURADA"):
        BASE_URL = 'https://www.hepsiburada.com/laptop-notebook-dizustu-bilgisayarlar-c-98?sayfa='

        for i in range(1, 13):
            sayfalink = BASE_URL + str(i)
            page_urls.append(sayfalink)
        for page in page_urls:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}
            r = requests.get(page, headers=headers)
            soup = BeautifulSoup(r.content, "lxml")

            st1 = soup.find("div", attrs={"class": "productListContent-pXUkO4iHa51o_17CBibU"})
            st2 = st1.find("ul", attrs={
                "class": "productListContent-frGrtf5XrVXRwJ05HUfU productListContent-rEYj2_8SETJUeqNhyzSm"})
            st3 = st2.find_all("li", attrs={"class": "productListContent-zAP0Y5msy8OHn5z7T_K_"})

            for linkler in st3:
                link_sonu = linkler.a.get("href")
                link_basi = "https://www.hepsiburada.com"
                link = link_basi + link_sonu

                if link_sonu.startswith("https://adservice"):
                    continue
                else:
                    comp_urls.append(link)


def insertDb(site, no):
    mydb = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-NR7S0A9;'
                          'Database=yazlabproje1;'
                          'Trusted_Connection=yes;')

    mycursor = mydb.cursor()

    ln = len(marka)
    for i in range(0, ln):
        idNo = str(no)
        if (site == "N11"):
            mycursor.execute(
                "INSERT INTO cimriinfos (urunId, isim, model, fiyat, site, link, resim) VALUES ('" + idNo + "','" +
                isim[i] + "','" + model[i] + "','" + fiyatN11[i] + "','" + site + "','" + listUniqueN11[i] + "','" +
                resim[i] + "')")
            mydb.commit()
            mycursor.execute(
                "INSERT INTO productinfos (urunId, isim, marka, model, isletimSistemi, islemciTipi, islemciNesli, ram, diskBoyutu, diskTuru, ekranBoyutu, puan, fiyat, site, link, resim) VALUES ('" + idNo + "','" +
                isim[i] + "','" + marka[i] + "','" + model[i] + "','"+ isletim_sis[i] + "','" + islemci_tipi[i] + "','" + islemci_nesli[i] + "','" + ram[i] + "','" + disk_boyutu[i] + "','" + disk_turu[i] + "','" + ekran_boyutu[i] + "','" +
                puanN11[i] + "','" + fiyatN11[i] + "','" + site + "','" + listUniqueN11[i] + "','" +resim[i] + "')")
            mydb.commit()
        elif (site == "TRENDYOL"):
            mycursor.execute(
                "INSERT INTO cimriinfos (urunId, isim, model, fiyat, site, link, resim) VALUES ('" + idNo + "','" +
                isim[i] + "','" + model[i] + "','" + fiyatTrendyol[i] + "','" + site + "','" + listUniqueTrendyol[i] + "','" +
                resim[i] + "')")
            mydb.commit()
            mycursor.execute(
                "INSERT INTO productinfos (urunId, isim, marka, model, isletimSistemi, islemciTipi, islemciNesli, ram, diskBoyutu, diskTuru, ekranBoyutu, puan, fiyat, site, link, resim) VALUES ('" + idNo + "','" +
                isim[i] + "','" + marka[i] + "','" + model[i] + "','" + isletim_sis[i] + "','" + islemci_tipi[i] + "','"+ islemci_nesli[i] + "','" +
                ram[i] + "','" + disk_boyutu[i] + "','" + disk_turu[i] + "','" + ekran_boyutu[i] + "','" + puanTrendyol[i] + "','" +
                fiyatTrendyol[i] + "','" + site + "','" + listUniqueTrendyol[i] + "','" + resim[i] + "')")
            mydb.commit()

        elif (site == "TEKNOSA"):
            mycursor.execute(
                "INSERT INTO cimriinfos (urunId, isim, model, fiyat, site, link, resim) VALUES ('" + idNo + "','" +
                isim[i] + "','" + model[i] + "','" + fiyatTeknosa[i] + "','" + site + "','" + listUniqueTeknosa[i] + "','" +
                resim[i] + "')")
            mydb.commit()
            mycursor.execute(
                "INSERT INTO productinfos (urunId, isim, marka, model, isletimSistemi, islemciTipi, islemciNesli, ram, diskBoyutu, diskTuru, ekranBoyutu, puan, fiyat, site, link, resim) VALUES ('" + idNo + "','" +
                isim[i] + "','" + marka[i] + "','" + model[i] + "','" + isletim_sis[i] + "','" + islemci_tipi[i] + "','" + islemci_nesli[i] + "','" +
                ram[i] + "','" + disk_boyutu[i] + "','" + disk_turu[i] + "','" + ekran_boyutu[i] + "','" + puanTeknosa[i] + "','" +
                fiyatTeknosa[i] + "','" + site + "','" + listUniqueTeknosa[i] + "','" + resim[i] + "')")
            mydb.commit()

        elif (site == "HEPSIBURADA"):
            mycursor.execute(
                "INSERT INTO cimriinfos (urunId, isim, model, fiyat, site, link, resim) VALUES ('" + idNo + "','" +
                isim[i] + "','" + model[i] + "','" + fiyatHepsiburada[i] + "','" + site + "','" + listUniqueHepsiburada[i] + "','" +
                resim[i] + "')")
            mydb.commit()
            mycursor.execute(
                "INSERT INTO productinfos (urunId, isim, marka, model, isletimSistemi, islemciTipi, islemciNesli, ram, diskBoyutu, diskTuru, ekranBoyutu, puan, fiyat, site, link, resim) VALUES ('" + idNo + "','" +
                isim[i] + "','" + marka[i] + "','" + model[i] + "','" + isletim_sis[i] + "','" + islemci_tipi[i] + "','" + islemci_nesli[i] + "','"+
                ram[i] + "','" + disk_boyutu[i] + "','" + disk_turu[i] + "','" + ekran_boyutu[i] + "','" + puanHepsiburada[i] + "','" +
                fiyatHepsiburada[i] + "','" + site + "','" + listUniqueHepsiburada[i] + "','" + resim[i] + "')")
            mydb.commit()
        no = no + 1
    return no


def truncateDb():
    mydb = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-NR7S0A9;'
                          'Database=yazlabproje1;'
                          'Trusted_Connection=yes;')

    mycursor = mydb.cursor()

    mycursor.execute("TRUNCATE TABLE cimriinfos")
    mydb.commit()
    mycursor.execute("TRUNCATE TABLE productinfos")
    mydb.commit()

def find_gen(model):
    if (('-' in model)):
        gen = model.split("-")

        if (gen[1].startswith("12")):
            return "12.NESİL"
        elif (gen[1].startswith("11")):
            return "11.NESİL"
        elif (gen[1].startswith("10")):
            return "10.NESİL"
        elif (gen[1].startswith("9")):
            return "9.NESİL"
        elif (gen[1].startswith("8")):
            return "8.NESİL"
        elif (gen[1].startswith("7")):
            return "7.NESİL"
        elif (gen[1].startswith("6")):
            return "6.NESİL"
        elif (gen[1].startswith("5")):
            return "5.NESİL"
        elif (gen[1].startswith("4")):
            return "4.NESİL"
        elif (gen[1].startswith("3")):
            return "3.NESİL"
    else:
        gen = islemci_model.split(" ")
        if (gen[3].startswith("N4")):
            return "4.NESİL"
        if (gen[3].startswith("N6")):
            return "6.NESİL"


listUniqueN11 = [
    'https://www.n11.com/urun/lenovo-thinkbook-15p-imh-20v3000vtx-i5-10300h-16-gb-512-gb-ssd-4-gb-gtx1650-156-dizustu-bilgisayar-2136271?magaza=os&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/lenovo-ip-gaming-3-82k100cwtx-i5-11300h-8-gb-1-tb256-gb-ssd-rtx3050-156-dos-tr-q-klavye-dizustu-bilgisayar-2875728?magaza=bozdanteknoloji&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/huawei-matebook-16-ryzen-7-5800h-16-gb-512-gb-16-w11h-dizustu-bilgisayar-4790654?magaza=ant-bilisim-a-s&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/acer-nitro-5-an515-45-nhqbaey005-r5-5600h-8-gb-512-gb-ssd-rtx3050-156-dos-dizustu-bilgisayar-5092260?magaza=teknoryabilisim&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/acer-nitro-5-an515-45-nhqbaey002-r5-5600h-8-gb-512-gb-ssd-rtx3050-144-hz-156-dos-dizustu-bilgisayar-2152318?magaza=teknoryabilisim&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/dell-inspiron-15-3511-i35111018u-i7-1165g7-16-gb-1-tb-hdd256-gb-ssd-mx350-156-ubuntu-fhd-dizustu-bilgisayar-5336936?magaza=gpnteknoloji&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/lenovo-thinkbook-15p-imh-20v3000stx-i5-10300h-16-gb-512-gb-ssd-gtx1650ti-156-free-dos-dizustu-bilgisayar-3096053?magaza=bizdeherseyvarki&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/lenovo-thinkpad-t14-g2-20w1s1mxtd-i7-1165g7-16-gb-512-gb-ssd-mx450-14-dos-fhd-dizustu-bilgisayar-7056179?magaza=teknoraks&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/lenovo-thinkpad-e15-g2-20td004ltx-i7-1165g7-16-gb-1-tb-ssd-mx450-156-dos-fhd-dizustu-bilgisayar-2086080?magaza=teknostok&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/hp-spectre-x360-4h1t0ea-i7-1165g7-16-gb-1-tb-ssd-135-w10h-touch-dizustu-bilgisayar-2126136?magaza=atesavm&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/asus-expertbook-b7-flip-b7402fea-l9017724-i7-1195g7-64-gb-2-tb-ssd-14-w10h-wqxga-dizustu-bilgisayar-17854805?magaza=b-t-teknoloji&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/msi-stealth-17m-a12ue-009xtr-i7-1280p-16-gb-512-gb-ssd-rtx3060-144hz-173-dos-dizustu-bilgisayar-13243013?magaza=kuantumsanal&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/acer-nitro-5-an515-45-nhqbaey004-r7-5800h-16-gb-512-gb-ssd-rtx3050-144hz-156-dos-dizustu-bilgisayar-2152263?magaza=teknoryabilisim&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/asus-expertbook-b7-flip-b7402fea-l9017732-i7-1195g7-64-gb-1-tb-ssd-14-w11p-wqxga-dizustu-bilgisayar-17854873?magaza=b-t-teknoloji&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/asus-rog-sitrix-g15-g513ic-hn095-r7-4800h-16-gb-1-tb-ssd-rtx3050-156-dos-fhd-dizustu-bilgisayar-18375431?magaza=gamers-arena&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/asus-expertbook-b7-flip-b7402fea-l901778-i7-1195g7-64-gb-1-tb-ssd-14-dos-wqxga-dizustu-bilgisayar-17854860?magaza=b-t-teknoloji&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/monster-abra-a5-v1828-i7-11800h-8-gb-500-gb-ssd-rtx3050ti-144hz-156-dos-german-keyboard-dizustu-bilgisayar-6698734?magaza=monster&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/apple-macbook-pro-mk1e3tua-apple-m1-pro-16-gb-512-gb-ssd-16-macos-dizustu-bilgisayar-2299711?magaza=centralteknoloji&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/apple-macbook-pro-mk183tua-apple-m1-pro-16-gb-512-gb-ssd-16-macos-dizustu-bilgisayar-2299691?magaza=exen&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/lenovo-ip-gaming-3-15ihu6-82k100cltx-i7-11370h-16-gb-1-tb256-rtx3050-156-dos-dizustu-bilgisayar-2940824?magaza=tekramarket&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/lenovo-thinkpad-p15v-21a9s02mtx-i7-11800h-16-gb-256-gb-ssd-t600-156-w10p-fhd-dizustu-bilgisayar-3660080?magaza=teknoraks&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/acer-nitro-5-an517-41-nhqarey001-r7-5800h-16-gb-512-gb-ssd-rtx3060-144hz-173-dos-dizustu-bilgisayar-2152264?magaza=teknoryabilisim&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/hp-15-ek1008nt-4h0h6ea-i7-10870h-16-gb-512-gb-ssd-rtx3070-156-free-dos-fhd-dizustu-bilgisayar-4318956?magaza=elmacik&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/msi-katana-gf76-11ud-059xtr-i7-11800h-16-gb-512-gb-ssd-4-gb-rtx3050ti-173-free-dos-dizustu-bilgisayar-1992518?magaza=techburada&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/msi-katana-gf76-11uc-638tr-i7-11800h-16-gb-512-gb-ssd-rtx3050-173-w11h-dizustu-bilgisayar-3771739?magaza=ebrarbilgisayar&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/hp-pavilion-15-ec2052nt-68n66ea-r7-5800h-16-gb-512-gb-rtx3050-144hz-156-dos-dizustu-bilgisayar-21289692?magaza=teknoryabilisim&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/monster-abra-a7-v141-i5-12500h-8-gb-500-gb-ssd-gtx1650-144-hz-173-free-dos-dizustu-bilgisayar-18715674?magaza=monster&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/hp-victus-16-e1005nt-68s21ea-ryzen-7-5800h-16gb-512gb-ssd-4gb-18057953?magaza=gpnteknoloji&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/lenovo-legion-5-82jh002jtx-i7-11600h-32-gb-512-gb-ssd-rtx3060-156-free-dos-wqhd-dizustu-bilgisayar-2691639?magaza=teknoraks&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/acer-nitro-5-an515-46-nhqgxey003-r7-6800h-16-gb-512-gb-ssd-rtx3050-156-dos-fhd-dizustu-bilgisayar-7431113?magaza=teknoryabilisim&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/excalibur-g9111198-dv80x-c-i9-11980hk-32-gb-500-gb-nvme-ssd-16-gb-rtx3080-16-dos-dizustu-bilgisayar-2104437?magaza=excalibur&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/asus-tuf-gaming-a15-fa507rm-hn095-r7-6800h-16-gb-512-gb-ssd-rtx3060-144hz-156-dos-dizustu-bilgisayar-10526522?magaza=gpnteknoloji&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/lenovo-legion-5-82jm0013tx-i7-11800h-16-gb-512-gb-rtx3060-144hz-173-dos-fhd-dizustu-bilgisayar-14692173?magaza=garajonline&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/msi-summit-e16-flip-a12uct-065tr-i7-1280p-16-gb-1-tb-ssd-rtx3050-16-w11p-qhd-touch-dizustu-bilgisayar-4133329?magaza=nesiltech&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/hp-zbook-fury-15-g8-314k1ea-i7-11850h-16-gb-512-gb-ssd-4-gb-rtx-a2000-156-w10p-dizustu-bilgisayar-2185556?magaza=vesmark&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/asus-tuf-gaming-a15-fa507rm-hn082-r7-6800h-16-gb-512-gb-ssd-rtx3060-144hz-156-dos-dizustu-bilgisayar-2574519?magaza=teknoryabilisim&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/msi-katana-gf76-11ue-470tr-i7-11800h-16-gb-1-tb-ssd-rtx3060-144hz-173-w11h-fhd-dizustu-bilgisayar-12788462?magaza=tekramarket&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/dell-m5760-tknm5760rks55h-w-11955m-32-gb-512-gb-ssd-a3000-17-w10p-uhd-touch-dizustu-bilgisayar-2750126?magaza=teknoraks&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/asus-rog-strix-g15-g513rm-hf266-r7-6800h-16-gb-512-gb-ssd-rtx3060-300hz-156-dos-dizustu-bilgisayar-11576167?magaza=gpnteknoloji&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/asus-rog-strix-g15-g513rm-hf267-r7-6800h-16-gb-512-gb-ssd-rtx3060-300hz-156-dos-dizustu-bilgisayar-10166602?magaza=teknoryabilisim&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/asus-rog-strix-g15-g513rm-hf265-r7-6800h-16-gb-512-gb-ssd-rtx3060-300hz-156-dos-dizustu-bilgisayar-7057945?magaza=gpnteknoloji&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/msi-delta-15-a5efk-096tr-r9-5900hx-32-gb-1-tb-ssd-rx6700m-240hz-156-w10h-fhd-dizustu-bilgisayar-2583416?magaza=nesiltech&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/asus-rog-strix-g15-g513rw-hf206-r7-6800h-16-gb-1-tb-ssd-rtx3070ti-300hz-156-dos-dizustu-bilgisayar-11167400?magaza=gpnteknoloji&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/msi-raider-ge77hx-12uhs-041tr-i9-12900hx-64-gb-2-tb-ssd-16-gb-rtx3080ti-173-w11h-dizustu-bilgisayar-10053444?magaza=nesiltech&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/msi-raider-ge77hx-12uhs-042tr-i7-12800hx-32-gb-2-tb-ssd-rtx3080ti-240hz-173-w11h-dizustu-bilgisayar-10526514?magaza=tekramarket&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/msi-stealth-gs66-12ugs-016tr-i7-12700h-32-gb-1-tb-ssd-rtx3070ti-156-w11h-dizustu-bilgisayar-2504443?magaza=nesiltech&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/msi-vector-gp76-12ugs-857tr-i9-12900h-32-gb-1-tb-ssd-rtx3070ti-173-free-dos-dizustu-bilgisayar-20269962?magaza=tekramarket&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/msi-vector-gp76-12uhso-869tr-i7-12700h-32-gb-1-tb-hdd-16-gb-rtx3080ti-173-dizustu-bilgisayar-23733872?magaza=nesiltech&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel',
    'https://www.n11.com/urun/msi-creator-m16-a12uc-226tr-i7-12700h-16-gb-1-tb-ssd-rtx3050-16-w11h-qhd-dizustu-bilgisayar-10121025?magaza=nesiltech&utm_source=comp_epey&utm_medium=cpc&utm_campaign=epey_genel'
    ]
listUniqueTrendyol = [
    'https://www.trendyol.com/lenovo/thinkbook-15p-20v3000vtx-i5-10300h-16gb-512gb-ssd-4gb-gtx1650-15-6-full-hd-freedos-p-147048280?boutiqueId=61&merchantId=351348&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/lenovo/ideapad-gaming-3-15ihu6-i5-11300h-8gb-256gb-ssd-1tb-hdd-rtx-3050-freedos-15-6-fhd-82k100cwtx-p-266086016?boutiqueId=613344&merchantId=107007&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/huawei/matebook-16-r7-5800h-16-512gb-gri-dizustu-bilgisayar-huawei-turkiye-garantili-p-287581690?boutiqueId=614790&merchantId=968&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/acer/nitro-5-an515-45-r5-5600h-8gb-512gb-ssd-rtx3050-dos-15-6-fhd-diuzstu-bilgisayar-nh-qbaey-005-p-302185457?boutiqueId=613344&merchantId=106740&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/acer/nitro-5-an515-45-ryzen-5-5600h-8-gb-512-gb-ssd-rtx-3050-144-hz-15-6-fhd-freedos-nh-qbaey-002-p-151476773?boutiqueId=613344&merchantId=106740&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/dell/inspiron-15-3511-i7-1165g7-16gb-ram-1tb-hdd-256gb-ssd-2gb-mx350-15-6-inc-fhd-ubuntu-i35111018u-p-303332683?boutiqueId=613344&merchantId=118442&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/lenovo/thinkbook-15p-20v3000stx-i5-10300h-16gb-512gb-ssd-4gb-gtx1650ti-15-6-fdos-p-270172576?boutiqueId=613344&merchantId=197602&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/lenovo/t14-20w1s1mxtd-i7-1165g7-16gb-512ssd-mx450-14-fullhd-freedos-tasinabilir-bilgisayar-p-305812697?boutiqueId=613344&merchantId=106664&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/lenovo/thinkpad-e15-20td004ltx-i7-1165g7-16gb-1tbssd-mx450-15-6-fullhd-freedos-tasinabilir-bilgisay-p-150776715?boutiqueId=613344&merchantId=105378&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/hp/spectre-x360-14-ea0008nt-4h1t0ea-i7-1165g7-16gb-ram-1tb-ssd-13-5-wuxga-dokunmatik-windows-10-p-143631717?boutiqueId=613344&merchantId=118442&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/asus/expertbook-i7-1195g7-64-gb-2-tbssd-iris-x-graphics-wqxga-14-w10home-b7402fea-l9017724-p-322551853?boutiqueId=613344&merchantId=107092&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/msi/nb-stealth-17m-a12ue-009xtr-i7-1280p-16gb-ddr4-rtx3060-gddr6-6gb-512gb-ssd-17-3-fhd-144hz-dos-p-317583075?boutiqueId=613344&merchantId=197602&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/acer/nitro-5-an515-45-amd-ryzen-7-5800h-16-gb-512-gb-ssd-rtx3050-144hz-15-6-fhd-freedos-nh-qbaey-004-p-151427013?boutiqueId=613344&merchantId=106740&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/asus/expertbook-i7-1195g7-64-gb-1-tbssd-iris-x-graphics-wqxga-14-w11pro-b7402fea-l9017732-p-322558387?boutiqueId=613344&merchantId=107092&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/asus/rog-strix-g15-g513ic-hn095-amd-ryzen-7-4800h-16gb-1tb-4gb-rtx3050-fhd-144hz-freedos-p-335445023?boutiqueId=613344&merchantId=105919&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/asus/expertbook-i7-1195g7-64-gb-1-tbssd-iris-x-graphics-wqxga-14-freedos-b7402fea-l901778-p-322551335?boutiqueId=613344&merchantId=107092&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/monster/abra-a5-v18-2-8-intel-core-i7-11800h-8gb-500gb-ssd-rtx3050ti-freedos-15-6-german-keyboard-p-307645892?boutiqueId=613344&merchantId=105286&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/apple/macbook-m1-pro-10c-cpu-16c-gpu-16gb-512gb-ssd-macos-16-qhd-gumus-laptop-apple-turkiye-garantili-p-179259323?boutiqueId=613344&merchantId=141868&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/apple/macbook-pro-16-m1-pro-16-gb-512gb-ssd-uzay-grisi-p-179245274?boutiqueId=61&merchantId=624588&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/lenovo/ideapad-gaming-3-82k100cltx-i7-11370h-16gb-1tb-256ssd-rtx3050-15-6-full-hd-freedos-tasinabili-p-294614443?boutiqueId=613344&merchantId=105013&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/lenovo/thinkpad-p15v-21a9s02mtx-i7-11800h-16gb-256ssd-t600-15-6-w10p-fullhd-tasinabilir-is-istasyon-p-277137113?boutiqueId=613344&merchantId=106664&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/acer/nitro-5-an517-41-amd-ryzen-7-5800h-16-gb-512-gb-ssd-rtx3060-144hz-17-3-fhd-freedos-nh-qarey-001-p-151463997?boutiqueId=61&merchantId=106740&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/hp/4h0h6ea-intel-core-i7-10870h-16gb-512-ssd-rtx3070-8gd6-15-6-fhd-ips-freedos-dizustu-bilgisayar-p-302598028?boutiqueId=613344&merchantId=109239&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/msi/katana-gf76-11ud-059xtr-i7-11800h-16gb-ddr4-rtx3050ti-gddr6-4gb-512gb-ssd-17-3-fhd-144hz-dos-p-105122726?boutiqueId=613344&merchantId=106740&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/msi/katana-gf76-11uc-638tr-i7-11800h-16gb-512gb-ssd-4gd6-17-3-fhd-144hz-w11-home-dizustu-bilgisayar-p-277323723?boutiqueId=613344&merchantId=105378&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/hp/pavilion-gaming-laptop-ryzen7-5800h-16gb-512gb-ssd-rtx3050-144hz-dos-15-6-fhd-notebook-68n66ea-p-346449429?boutiqueId=613344&merchantId=106740&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/monster/abra-a7-v14-1-intel-core-i5-12500h-8-gb-ram-500gb-ssd-4gb-gtx1650-freedos-17-3-fhd-144hz-p-343040585?boutiqueId=613344&merchantId=105286&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/hp/victus-16-e1005nt-68s21ea-ryzen-7-6800h-16gb-ram-512gb-ssd-4gb-rtx3050ti-16-1-fhd-144hz-p-331929784?boutiqueId=613344&merchantId=118442&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/lenovo/legion-5-82jh002jtx-i7-11600h-32gb-512ssd-rtx3060-15-6-wqhd-freedos-tasinabilir-bilgisayar-p-251038225?boutiqueId=613901&merchantId=106664&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/acer/nitro-5-an515-46-amd-ryzen-7-6800h-16-gb-512-gb-ssd-rtx3050-dos-15-6-fhd-notebook-nh-qgxey-003-p-308104228?boutiqueId=61&merchantId=106740&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/casper/excalibur-g911-1198-dv80x-c-intel-11-nesil-i9-11980hk-32gb-ram-500gb-nvme-ssd-16gb-rtx3080-freedos-p-131487472?boutiqueId=613344&merchantId=114258&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/asus/tuf-gaming-a15-fa507rm-hn095-ryzen-7-6800h-16gb-ram-512gb-ssd-6gb-rtx3060-15-6-inc-fhd-144hz-p-322587921?boutiqueId=613344&merchantId=118442&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/lenovo/legion5intel-corei7-11800h-16gb-512gb-ssd-rtx3060-6gb-dos-17-3-fhd-82jm0013tx-p-329375305?boutiqueId=613344&merchantId=124551&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/msi/summit-e16-flip-a12uct-065tr-i7-1280p-16gb-lpddr5-rtx3050-gddr6-6gb-1tb-ssd-16-qhd-165hz-touch-p-282824564?boutiqueId=613344&merchantId=106740&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/hp/zbook-fury-15-g8-314k1ea-i7-11850h-16gb-512ssd-a2000-15-6-w10p-tasinabilir-is-istasyonu-p-238851925?boutiqueId=613901&merchantId=106664&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/asus/tuf-gaming-a15-fa507rm-hn082-ryzen7-6800h-16gb-512gb-ssd-rtx3060-144hz-dos-15-6-fhd-notebook-p-239402022?boutiqueId=613344&merchantId=106740&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/msi/katana-gf76-11ue-470tr-i7-11800h-16gb-ram-1tb-ssd-6gb-rtx3060-17-3-fhd-144hz-w11-p-314123074?boutiqueId=613344&merchantId=105013&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/dell/m5760-tknm5760rks55h-w-11955m-32gb-512ssd-a3000-17-uhd-touch-w10p-tasinabilir-is-istasyonu-p-310908864?boutiqueId=613901&merchantId=106664&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/asus/rog-strix-g15-g513rm-hf266-ryzen-7-6800h-16gb-ddr5-ram-512gb-ssd-6gb-rtx3060-15-6-inc-fhd-300hz-p-322587816?boutiqueId=613344&merchantId=118442&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/asus/rog-strix-g15-g513rm-hf267-ryzen-7-6800h-16gb-512gb-ssd-rtx3060-300hz-dos-15-6-fhd-notebook-p-311539393?boutiqueId=613344&merchantId=106740&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/asus/rog-strix-g15-g513rm-hf265-ryzen-7-6800h-16gb-ddr5-ram-512gb-ssd-6gb-rtx3060-15-6-fhd-300hz-p-311018697?boutiqueId=613344&merchantId=118442&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/msi/delta-15-a5efk-096tr-r9-5900hx-32gb-ddr4-rx6700m-gddr6-10gb-1tb-ssd-15-6-fhd-240hz-w10-p-235902367?boutiqueId=613344&merchantId=106740&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/asus/rog-strix-g15-g513rw-hf206-ryzen-7-6800h-16gb-ddr5-ram-1tb-ssd-8gb-rtx3070ti-15-6-fhd-300hz-p-313749564?boutiqueId=613344&merchantId=118442&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/msi/raider-ge77hx-12uhs-041tr-i9-12900hx-64gb-ddr5-rtx3080ti-gddr6-16gb-2tb-ssd-17-3-uhd-120hz-w11-p-313386246?boutiqueId=61&merchantId=197602&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/msi/raider-ge77hx-12uhs-042tr-i7-12800hx-32gb-ddr5-rtx3080ti-gddr6-16gb-2tb-ssd-17-3-qhd-240hz-w11-p-312669810?boutiqueId=61&merchantId=197602&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/msi/stealth-gs66-12ugs-016tr-i7-12700h-32gb-ddr5-rtx3070ti-gddr6-8gb-1tb-ssd-15-6-qhd-240hz-w11-p-230344887',
    'https://www.trendyol.com/msi/vector-gp76-12ugs-857tr-i9-12900h-32gb-ddr4-rtx3070ti-gddr6-8gb-1tb-ssd-17-3-fhd-144hz-w11h-p-345570368?boutiqueId=613344&merchantId=106740&utm_source=aff_t',
    'https://www.trendyol.com/msi/vector-gp76-12uhso-869tr-i7-12700h-32gb-ddr4-rtx3080ti-gddr6-16gb-1tb-ssd-17-3-fhd-360hz-w11-p-356078147?boutiqueId=61&merchantId=106198&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme',
    'https://www.trendyol.com/msi/creator-m16-a12uc-226tr-i7-12700h-16gb-ddr4-rtx3050-gddr6-4gb-1tb-ssd-16-0-qhd-w11-p-309008730?boutiqueId=613344&merchantId=106198&v=tek-ebat&utm_source=aff_t&utm_medium=cpc&utm_campaign=epey_urun_listeleme&adjust_tracker=uv21fv4_za1u3cm&adjust_campaign=epey_urun_listeleme'

    ]
listUniqueTeknosa = [
    'https://www.teknosa.com/lenovo-thinkbook-15p-20v3000vtx-i510300h-16-gb-512-gb-ssd-4-gb-gtx1650-156-full-hd-freedos-tasinabilir-bilgisayar-p-786280558?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/lenovo-ideapad-gaming-3-15ihu6-82k100cwtx-i5-11300h-156-8-gb-ram-256-gb-ssd-1-tb-hdd-rtx3050-fhd-freedos-tasinabilir-bilgisayar-p-786280266?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/huawei-matebook-16-amd-ryzen-7-5800h-16gb-ram-512-gb-ssd-16-fhd-w11-notebook-p-125034352?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/acer-nitro-5-an51545-nhqbaey005-amd-ryzen-5-5600h-8-gb-512-gb-ssd-rtx-3050-freedos-156-fhd-tasinabilir-bilgisayar-p-785350507?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/acer-nitro-5-an51545-nhqbaey002-ryzen-5-5600h-156-8-gb-ram-512-gb-ssd-rtx3050-fhd-freedos-tasinabilir-bilgisayar-p-785350360?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/dell-inspiron-15-3511-i35111018u-i71165g7-156-16-gb-1-tb-hdd256-gb-ssd-2-gb-mx350-fhd-ubuntu-tasinabilir-bilgisayar-p-786280756?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/lenovo-thinkbook-15p-20v3000stx-intel-core-i510300h-156-16-gb-512-gb-ssd-4-gb-gtx1650ti-freedos-tasinabilir-bilgisayar-p-786280821?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/lenovo-t14-20w1s1mxtd-intel-core-i71165g7-14-16-gb-ram-512-gb-ssd-mx450-full-hd-freedos-tasinabilir-bilgisayar-p-786280934?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/lenovo-thinkpad-e15-20td004ltx-intel-core-i7-1165g7-156-16-gb-ram-1-tb-ssd-2-gb-mx450-fhd-freedos-tasinabilir-bilgisayar-p-786282229?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/hp-spectre-x360-14ea0008nt-4h1t0ea-intel-core-i71165g7-135-16-gb-ram-1-tb-ssd-wuxgadokunmatik-windows-10-laptop-p-786280184?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/asus-expertbook-b7402feal9017724-intel-core-i71195g7-14-64-gb-ram-2-tb-w10home-tasinabilir-bilgisayar-p-786281617?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/msi-stealth-17m-a12ue009xtr-i71280p-16-gb-ram-512-gb-ssd-6-gb-rtx3060-173-fhd-144-hz-freedos-gaming-laptop-p-785351505?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/acer-nitro-5-an51545-nhqbaey004-amd-ryzen-75800h-156-16-gb-ram-512-gb-ssd-rtx3050-freedos-156-fhd-laptop-p-786280155?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/asus-expertbook-b7402feal9017732-intel-core-i71195g7-14-64-gb-ram-1-tb-ssdw11pro-tasinabilir-bilgisayar-p-786281601?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/asus-rog-strix-g15-g513ichn096-amd-ryzen-7-4800h-16-gb-1-tb-ssd-rtx3050-144-hz-freedos-156-fhd-tasinabilir-bilgisayar-p-785351256?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/asus-expertbook-b7402feal901778-intel-core-i71195g7-14-64-gb-ram-1-tb-ssd-freedos-tasinabilir-bilgisayar-p-786281584?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/monster-abra-a5-v1828-intel-core-i7-11800h-8-gb-500-gb-ssd-rtx3050ti-freedos-156-fhd-german-keyboard-gaming-laptop-p-785351047?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/apple-macbook-pro-m1-pro-cip-10c-512gb-ssd-16-gumus-dizustu-bilgisayar-mk1e3tua-p-125034258?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/apple-macbook-pro-m1-pro-cip-10c-512gb-ssd-16-uzay-grisi-dizustu-bilgisayar-mk183tua-p-125034255?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/lenovo-ideapad-gaming-3-82k100cltx-i711370h-16-gb-1-tb-256-gb-ssd-rtx3050-156-full-hd-freedos-tasinabilir-bilgisayar-p-785350604?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/lenovo-thinkpad-p15v-21a9s02mtx-i711800h-156-16-gb-256-ssd-t600-w10p-full-hd-tasinabilir-bilgisayar-p-786280716?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/acer-nitro-5-an51741-nhqarey001-amd-ryzen-7-5800h-16-gb-512-gb-ssd-rtx-3060-144-hz-173-fhd-freedos-laptop-p-786280165?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/hp-15ek1008nt-4h0h6ea-i710870h-16-gb-512-gb-ssd-8-gb-rtx3070-156-fhd-144-hz-freedos-tasinabilir-bilgisayar-p-786280548?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/msi-katana-gf76-11ud059xtr-intel-core-i7-11800h-173-16-gb-ram-512-gb-ssd-tx3050ti-fhd-freedos-laptop-p-786280114?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/msi-katana-gf76-11uc638tr-i711800h-16-gb-512-gb-ssd-4-gb-rtx3050-173-fhd-144-hz-windows-11-tasinabilir-bilgisayar-p-786280544?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/hp-pavilion-gaming-15ec2052nt-68n66ea-amd-ryzen-7-5800h-156-16-gb-ram-512-gb-ssd-rtx-3050-144-hz-fhd-freedos-laptop-p-785352613?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/monster-abra-a7-v141-intel-core-i5-12500h-173-8-gb-ram-500-gb-ssd-nvidia-geforce-gtx-1650-fhd-freedos-gaming-laptop-p-785352019?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/hp-victus-16e1005nt-68s21ea-amd-ryzen-7-6800h-161-fhd-16-gb-ram-512-gb-ssd-144-hz-tasinabilir-bilgisayar-p-785351800?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/lenovo-legion-5-82jh002jtx-i711600h-32-gb-512-ssd-rtx3060-156-wqhd-freedos-tasinabilir-bilgisayar-p-786280703?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/acer-nitro-5-an51546-nhqgxey003-amd-ryzen-7-6800h-156-16-gb-ram-512-gb-ssd-rtx-3050-freedos-gaming-laptop-p-785352902?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/casper-excalibur-g9111198dv80xc-intel-core-i911980hk-32-gb-ram-500-gb-nvme-ssd-16-gb-rtx3080-freedos-p-785350027?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/asus-tuf-gaming-a15-fa507rmhn095-ryzen-7-6800h-16-gb-ram-512-gb-ssd-6-gb-rtx3060-156-fhd-144-hz-tasinabilir-bilgisayar-p-785351266?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/lenovo-legion-5-82jh002jtx-i711600h-32-gb-512-ssd-rtx3060-156-wqhd-freedos-tasinabilir-bilgisayar-p-786280703',
    'https://www.teknosa.com/msi-summit-e16-flip-a12uct065tr-i71280p-16-16-gb-1-tb-ssd-4-gb-rtx3050-qhd-touch-windows-11-pro-tasinabilir-bilgisayar-p-786280759?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/hp-zbook-fury-15-g8-314k1ea-i711850h-16-gb-512-gb-ssd-a2000-156-w10p-tasinabilir-bilgisayar-p-786280373?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/asus-tuf-gaming-a15-fa507rmhn082-amd-ryzen-7-6800h-16-gb-512-gb-ssd-rtx-3060-144-hz-freedos-156-fhd-tasinabilir-bilgisayar-p-785351132?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/msi-katana-gf76-11ue470tr-intel-core-i7-11800h-173-16-gb-ram-1-tb-ssd-6-gb-rtx-3060-fhd-144-hz-windows-11-gaming-laptop-p-785352881?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/dell-m5760-tknm5760rks55h-w11955m-32-gb-512-gb-ssd-a3000-17-uhd-touch-w10p-tasinabilir-bilgisayar-p-786280391?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/asus-rog-strix-g15-g513rmhf266-ryzen-7-6800h-16-gb-ddr5-ram-512-gb-ssd-6-gb-rtx3060-156-fhd-300-hz-tasinabilir-bilgisayar-p-785351364?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/asus-rog-strix-g15-g513rmhf267-amd-ryzen-7-6800h-16-gb-512-gb-ssd-rtx-3060-300-hz-freedos-156-fhd-tasinabilir-bilgisayar-p-785351255?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/asus-rog-strix-g15-g513rmhf265-ryzen-7-6800h-16-gb-ddr5-ram-512-gb-ssd-6-gb-rtx3060-156-fhd-300-hz-gaming-laptop-p-785351040?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/msi-delta-15-a5efk096tr-r95900hx-32-gb-ram-1-tb-ssd-10-gb-rx6700m-156-fhd-240-hz-w10-laptop-p-786280128?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/asus-rog-strix-g15-g513rwhf206-ryzen-7-6800h-16-gb-ddr5-ram-1-tb-ssd-8-gb-rtx3070ti-156-fhd-300-hz-p-785351504?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/msi-raider-ge77hx-12uhs041tr-i912900hx-64-gb-2-tb-ssd-16-gb-rtx3080ti-173-uhd-120-hz-windows-11-tasinabilir-bilgisayar-p-786281111?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/msi-raider-ge77hx-12uhs042tr-i712800hx-32-gb-2-tb-ssd-16-gb-rtx3080ti-173-qhd-240-hz-windows-11tasinabilir-bilgisayar-p-786281199?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/msi-stealth-gs66-12ugs016tr-intel-core-i7-12700h-32-gb-1-tb-ssd-rtx3070ti-windows-11-home-156-gaming-laptop-p-785350207?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/msi-vector-gp76-12ugs857tr-intel-core-i9-12900h-173-32-gb-ram-1-tb-ssd-8-gb-rtx-3070-ti-windows-11-fhd-tasinabilir-bilgisayar-p-786282069?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/msi-vector-gp76-12uhso869tr-intel-core-i712700h-173-32-gb-ram-1-tb-ssd-16-gb-rtx-3080-ti-fhd-360-hz-freedos-gaming-laptop-p-785353202?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',
    'https://www.teknosa.com/msi-creator-m16-a12uc226tr-intel-core-i712700h-16-16-gb-1-tb-ssd-4-gb-rtx3050-qhd-windows-11-tasinabilir-bilgisayar-p-786280876?ref=go&utm_source=go&utm_medium=affiliate&utm_campaign=21',

    ]
listUniqueHepsiburada = [
    'https://www.hepsiburada.com/lenovo-thinkbook-15p-intel-core-i5-10300h-16-gb-512-gb-ssd-gtx1650-free-dos-15-6-fhd-tasinabilir-bilgisayar-20v3000vtx-p-HBCV00000S2AZJ?magaza=OS%20B%C4%B0L%C4%B0%C5%9E%C4%B0M&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00000S2AZJ&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/lenovo-ideapad-gaming-3-15ihu6-intel-core-i5-11300h-8gb-256gb-ssd-1tb-hdd-rtx-3050-freedos-15-6-fhd-tasinabilir-bilgisayar-82k100cwtx-p-HBCV00001VDMED?magaza=BOZDAN%20Teknoloji&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00001VDMED&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/huawei-matebook-16-amd-ryzen-7-5800h-16gb-512gb-ssd-windows-11-home-16-ips-tasinabilir-bilgisayar-p-HBCV000020V9FE?magaza=OZERPA%20PAZARLAMA&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV000020V9FE&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/acer-nitro-5-an515-45-amd-ryzen-5-5600h-8-gb-512-gb-ssd-rtx-3050-freedos-15-6-fhd-144-hz-tasinabilir-bilgisayar-nh-qbaey-005-p-HBCV000028L2HB?magaza=Teknorya&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV000028L2HB&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/acer-nitro-5-an515-45-ryzen-5-5600h-8gb-512gb-ssd-rtx3050-freedos-15-6-fhd-tasinabilir-bilgisayar-nh-qbaey-002-p-HBCV00000RF4Z1?magaza=Teknorya&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00000RF4Z1&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/dell-inspiron-15-3511-intel-core-i7-1165g7-16gb-1-tb-hdd-256gb-ssd-mx350-ubuntu-15-6-fhd-tasinabilir-bilgisayar-i35111018u-p-HBCV000029758V?magaza=GpnTeknoloji&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV000029758V&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/lenovo-thinkbook-15p-20v3000stx-i5-10300h-16gb-512gb-ssd-4gb-gtx1650ti-freedos-15-6-tasinabilir-bilgisayar-p-HBCV00001XW4HL?magaza=Kuantum&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00001XW4HL&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/lenovo-t14-20w1s1mxtd-i7-1165g7-16gb-512ssd-mx450-14-fullhd-freedos-tasinabilir-bilgisayar-p-HBCV00002CCC90?magaza=teknoraks&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00002CCC90&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/lenovo-thinkpad-e15-gen-2-intel-core-i7-1165g7-16gb-1tb-ssd-2gb-mx450-freedos-15-6-fhd-tasinabilir-bilgisayar-20td004ltx-p-HBCV00000EUOA2?magaza=notebookstore&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00000EUOA2&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/hp-spectre-x360-14-ea0008nt-intel-core-i7-1165g7-16gb-1tb-ssd-windows-10-home-13-5-tasinabilir-bilgisayar-4h1t0ea-p-HBCV00000N9TCW?magaza=alsabilisim&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00000N9TCW&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/asus-exper-tbook-intel-core-i7-1195g7-64-gb-2-tb-ssd-iris-x-graphics-windows-10-home-14-fhd-tasinabilir-bilgisayar-b7402fea-l9017724-p-HBCV00002LFMOC?magaza=BT%20Teknoloji&utm_campaign=c&utm_content=HBCV00002LFMOC&utm_medium=epey&utm_source=pc&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/msi-stealth-17m-a12ue-009xtr-intel-core-i7-1280p-16gb-512gb-ssd-rtx3060-freedos-17-3-fhd-144hz-tasinabilir-bilgisayar-p-HBCV00002G7ZPS?magaza=Kuantum&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00002G7ZPS&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/acer-nitro-5-an515-45-amd-ryzen-7-5800h-16gb-512gb-ssd-rtx3050-freedos-15-6-fhd-tasinabilir-bilgisayar-nh-qbaey-004-p-HBCV00000RF4Z5?magaza=Teknorya&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00000RF4Z5&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/asus-exper-tbook-intel-core-i7-1195g7-64-gb-1-tb-ssd-iris-x-graphics-windows-11-pro-14-fhd-tasinabilir-bilgisayar-b7402fea-l9017732-p-HBCV00002LFMOA?magaza=BT%20Teknoloji&utm_campaign=c&utm_content=HBCV00002LFMOA&utm_medium=epey&utm_source=pc&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/asus-rog-strix-g15-g513ic-hn096-amd-ryzen-7-4800h-16gb-1-tb-ssd-rtx3050-144-hz-freedos-15-6-fhd-tasinabilir-bilgisayar-p-HBCV00002ERGXZ?magaza=Teknorya&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00002ERGXZ&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/asus-exper-tbook-intel-core-i7-1195g7-64-gb-1-tb-ssd-iris-x-graphics-freedos-14-fhd-tasinabilir-bilgisayar-b7402fea-l901778-p-HBCV00002LFMOM?magaza=BT%20Teknoloji&utm_campaign=c&utm_content=HBCV00002LFMOM&utm_medium=epey&utm_source=pc&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/monster-abra-a5-v18-2-8-intel-core-i7-11800h-8gb-500gb-ssd-rtx-3050ti-freedos-15-6-fhd-almanca-klavye-tasinabilir-bilgisayar-p-HBCV00002CTB4T?magaza=Monster%20Notebook&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00002CTB4T&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/apple-macbook-m1-pro-cip-16gb-512gb-ssd-macos-16-qhd-tasinabilir-bilgisayar-gumus-mk1e3tu-a-p-HBCV00000U6XEF?magaza=Hepsiburada&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00000U6XEF&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/apple-macbook-m1-pro-cip-16gb-512gb-ssd-macos-16-qhd-tasinabilir-bilgisayar-uzay-grisi-mk183tu-a-p-HBCV00000U6WE5?magaza=Bsz%20Elektronik&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00000U6WE5&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/lenovo-ideapad-gaming-3-82k100cltx-intel-core-i7-11370h-16gb-1tb-256-ssd-rtx3050-15-6-fhd-freedos-tasinabilir-bilgisayar-p-HBCV0000276SAU?magaza=Tekramarket&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV0000276SAU&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/lenovo-thinkpad-p15v-21a9s02mtx-i7-11800h-16gb-256ssd-t600-15-6-windows-10-pro-fhd-tasinabilir-bilgisayar-p-HBCV000020Z32N?magaza=teknoraks&utm_campaign=c&utm_content=HBCV000020Z32N&utm_medium=epey&utm_source=pc&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/acer-nitro-5-an517-41-amd-ryzen-7-5800h-16gb-512gb-ssd-rtx3060-freedos-17-3-fhd-tasinabilir-bilgisayar-nh-qarey-001-p-HBCV00000RF4Z7?magaza=Teknorya&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00000RF4Z7&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/hp-omen-15-ek1008nt-intel-core-i7-10870h-16gb-512gb-ssd-rtx3070-freedos-15-6-tasinabilir-bilgisayar-4h0h6ea-p-HBCV00001955C1?magaza=Elmac%C4%B1k&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00001955C1&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/msi-katana-gf76-11ud-059xtr-intel-core-i7-11800h-16gb-512gb-ssd-rtx-3050ti-freedos-17-3-fhd-tasinabilir-bilgisayar-p-HBCV000006G7VU?magaza=Teknorya&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV000006G7VU&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/msi-katana-gf76-11uc-638tr-intel-core-i7-11800h-16gb-512gb-ssd-rtx3050-17-3-fhd-windows-11-home-tasinabilir-bilgisayar-p-HBCV00002928J3?magaza=Ebrar%20Bilgisayar&utm_campaign=c&utm_content=HBCV00002928J3&utm_medium=epey&utm_source=pc&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/hp-pavilion-gaming-laptop-15-ec2052nt-amd-ryzen-7-5800h-16-gb-512-gb-ssd-rtx-3050-144-hz-freedos-15-6-fhd-tasinabilir-bilgisayar-68n66ea-p-HBCV00002UM64S?magaza=Teknorya&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00002UM64S&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/monster-abra-a7-v14-1-intel-core-i5-12500h-8gb-ram-500gb-ssd-4gb-gtx1650-freedos-17-3-fhd-144hz-oyun-bilgisayari-p-HBCV00002RJF1Z?magaza=Monster%20Notebook&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00002RJF1Z&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/hp-victus-16-e1005nt-68s21ea-ryzen-7-6800h-16gb-ram-512gb-ssd-4gb-rtx3050ti-16-1-fhd-144hz-tasinabilir-bilgisayar-p-HBCV00002Q5W79?magaza=GpnTeknoloji&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00002Q5W79&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/lenovo-legion-5-82jh002jtx-intel-core-i7-11600h-32gb-512-ssd-rtx3060-15-6-wqhd-freedos-tasinabilir-bilgisayar-p-HBCV00001P97QQ?magaza=teknoraks&utm_campaign=c&utm_content=HBCV00001P97QQ&utm_medium=epey&utm_source=pc&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/acer-nitro-5-an515-46-amd-ryzen-7-6800h-16-gb-512-gb-ssd-rtx-3050-freedos-15-6-fhd-tasinabilir-bilgisayar-nh-qgxey-003-p-HBCV00002EFBNS?magaza=Teknorya&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00002EFBNS&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/casper-excalibur-g911-1198-dv80x-c-intel-core-i9-11980hk-32gb-500gb-nvme-ssd-rtx3080-freedos-tasinabilir-bilgisayar-p-HBCV00000ICRRK?magaza=EXCALIBUR&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00000ICRRK&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/asus-tuf-gaming-a15-fa507rm-hn095-ryzen-7-6800h-16gb-512gb-ssd-rtx-3060-144-hz-freedos-15-6-fhd-tasinabilir-bilgisayar-p-HBCV00002GIDW2?magaza=GpnTeknoloji&utm_campaign=c&utm_content=HBCV00002GIDW2&utm_medium=epey&utm_source=pc&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/lenovo-legion-5-intel-core-i7-11800h-16gb-512gb-ssd-rtx3060-freedos-17-3-fhd-tasinabilir-bilgisayar-82jm0013tx-p-HBCV00002LBY9Z?magaza=GarajOnline&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00002LBY9Z&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/msi-summit-e16-flip-a12uct-065tr-intel-core-i7-1280p-16gb-1tb-ssd-rtx3050-windows-11-pro-16-165hz-tasinabilir-bilgisayar-p-HBCV000022W8XR?magaza=Techburada&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV000022W8XR&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/hp-zbook-fury-g8-intel-core-i7-11850h-16gb-512gb-ssd-rtx-a2000-windows-10-pro-15-6-fhd-tasinabilir-is-istasyonu-314k1ea-p-HBCV00000ZHB6O?magaza=Vesmark&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00000ZHB6O&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/asus-tuf-gaming-a15-fa507rm-hn082-amd-ryzen-7-6800h-16-gb-512-gb-ssd-rtx-3060-144-hz-freedos-15-6-fhd-tasinabilir-bilgisayar-p-HBCV00001ET5UY?magaza=Teknorya&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00001ET5UY&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/msi-katana-gf76-11ue-470tr-intel-core-i7-11800h-16gb-1tb-ssd-rtx3060-windows-11-home-17-3-fhd-144hz-tasinabilir-bilgisayar-p-HBCV00002G7ZPO?magaza=Tekramarket&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00002G7ZPO&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/dell-m5760-tknm5760rks55h-w-11955m-32gb-512ssd-a3000-17-uhd-touch-windows-10-pro-tasinabilir-tasinabilir-bilgisayar-p-HBCV00001TKIAH?magaza=teknoraks&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00001TKIAH&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/asus-rog-strix-g15-g513rm-hf266-ryzen-7-6800h-16gb-ddr5-ram-512gb-ssd-6gb-rtx3060-15-6-inc-fhd-300hz-tasinabilir-bilgisayar-p-HBCV00002H2C73?magaza=GpnTeknoloji&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00002H2C73&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/asus-rog-strix-g15-g513rm-hf267-amd-ryzen-7-6800h-16-gb-512-gb-ssd-rtx-3060-300-hz-freedos-15-6-fhd-tasinabilir-bilgisayar-p-HBCV00002ERGXX?magaza=Teknorya&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00002ERGXX&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/asus-rog-strix-g15-g513rm-hf265-ryzen-7-6800h-16gb-ddr5-ram-512gb-ssd-6gb-rtx3060-15-6-fhd-300hz-tasinabilir-bilgisayar-p-HBCV00002D5X2N?magaza=GpnTeknoloji&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00002D5X2N&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/msi-delta-15-a5efk-096tr-amd-ryzen-9-5900hx-rx6700m-32gb-1tb-ssd-rx6700m-windows-11-home-15-6-fhd-tasinabilir-bilgisayar-p-HBCV00001G032Q?magaza=Emperor&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00001G032Q&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/asus-rog-strix-g15-g513rw-hf206-ryzen-7-6800h-16gb-ddr5-ram-1tb-ssd-8gb-rtx3070ti-15-6-inc-fhd-300hz-tasinabilir-bilgisayar-p-HBCV00002GRKL7?magaza=GpnTeknoloji&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00002GRKL7&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/msi-raider-ge77hx-12uhs-041tr-intel-core-i9-12900hx-64gb-2tb-ssd-rtx3080ti-windows-11-home-17-3-uhd-120hz-tasinabilir-bilgisayar-p-HBCV00002G7SXS?magaza=GpnTeknoloji&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00002G7SXS&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/msi-raider-ge77hx-12uhs-042tr-intel-core-i7-12800hx-32gb-2tb-ssd-rtx3080ti-windows-11-home-17-3-qhd-240hz-tasinabilir-bilgisayar-p-HBCV00002G7SXQ?magaza=Kuantum&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00002G7SXQ&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/msi-stealth-gs66-12ugs-016tr-intel-core-i7-12700h-32gb-1tb-ssd-rtx3070ti-windows-11-home-15-6-tasinabilir-bilgisayar-p-HBCV00001BWPTE?magaza=GpnTeknoloji&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00001BWPTE&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/msi-vector-gp76-12ugs-857tr-intel-core-i9-12900h-32gb-1tb-ssd-rtx3070ti-windows-11-home-17-3-fhd-144hz-tasinabilir-bilgisayar-p-HBCV00002TOK2U?magaza=Kuantum&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00002TOK2U&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/msi-vector-gp76-12uhso-869tr-intel-core-i7-12700h-32gb-1tb-ssd-rtx3080ti-windows-11-home-17-3-fhd-360hz-tasinabilir-bilgisayar-p-HBCV00002XZGW6?magaza=Techburada&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00002XZGW6&utm_term=c&wt_pc=epey.c.c.c',
    'https://www.hepsiburada.com/msi-creator-m16-a12uc-226tr-intel-core-i7-12700h-16gb-1tb-ssd-rtx3050-windows-11-home-16-qhd-tasinabilir-bilgisayar-p-HBCV00002BP756?magaza=GpnTeknoloji&utm_source=pc&utm_medium=epey&utm_campaign=c&utm_content=HBCV00002BP756&utm_term=c&wt_pc=epey.c.c.c'
    ]

fiyatTrendyol = []
puanTrendyol = []
fiyatN11 = []
puanN11 = []
fiyatTeknosa = []
puanTeknosa = []
fiyatHepsiburada = []
puanHepsiburada = []

marka = []
model = []
isletim_sis = []
islemci_tipi = []
islemci_nesli = []
ram = []
disk_boyutu = []
disk_turu = []
ekran_boyutu = []
isim = []
resim = []

no = 1

truncateDb()

for k in listUniqueN11:
    soup = get_soup(k)

    try:
        title = soup.find("div", {"class": "unf-p-summary-price"}).text
        title = title.replace(".", "")
        fiyatN11.append(title)
        image = soup.find("div", {"class": "items"})
        resim.append(image.img["data-lazy"])

        rating = soup.find("strong", {"class": "ratingScore"})
        x = rating.text
        if ('.' in x):
            puanN11.append(x)
        else:
            temp = x + ".0"
            puanN11.append(temp)

        title = soup.find("h1", {"class": "proName"}).text.strip()
        title = title.upper()
        isim.append(title)

        title = soup.find_all("li", {"class": "unf-prop-list-item"})

        control = 0
        for data in title:

            if ('Marka' in data.text):
                temp = data.a.text.strip()
                temp = temp.upper()
                marka.append(temp)

            elif ('İşletim Sistemi' in data.text):
                temp = data.find("p", {"class": "unf-prop-list-prop"}).text.strip()
                temp = temp.upper()
                isletim_sis.append(temp)

            elif ('Disk Kapasitesi' in data.text):
                temp = data.find("p", {"class": "unf-prop-list-prop"}).text.strip()
                temp = temp.upper()
                a = 0
                b = 0
                if ('+' in temp):
                    temp1 = temp.split("+")
                    for i in temp1:
                        if ('TB' in i):
                            temp2 = i.split(" ")
                            temp2 = temp2[0]
                            a = a + (int(temp2) * 1024)
                        elif ('GB' in i):
                            temp2 = i.split(" ")
                            temp2 = temp2[1]
                            b = b + int(temp2)
                    temp = a + b
                    temp = str(temp) + " GB"
                disk_boyutu.append(temp)

            elif ('Ekran Boyutu' in data.text):
                temp = data.find("p", {"class": "unf-prop-list-prop"}).text.strip()
                temp = temp.upper()
                ekran_boyutu.append(temp)

            elif ('Disk Türü' in data.text):
                control = 1
                temp = data.find("p", {"class": "unf-prop-list-prop"}).text.strip()
                temp = temp.upper()
                disk_turu.append(temp)

            elif ('Bellek Kapasitesi' in data.text):
                temp = data.find("p", {"class": "unf-prop-list-prop"}).text.strip()
                temp = temp.upper()
                ram.append(temp)

            elif (('İşlemci' in data.text) & ('Modeli' not in data.text) & ('Hızı' not in data.text) & (
                    'Çekirdek' not in data.text)):
                temp = data.find("p", {"class": "unf-prop-list-prop"}).text.strip()
                temp = temp.upper()
                islemci_tipi.append(temp)

            elif (('İşlemci Modeli' in data.text)):
                islemci_model = data.find("p", {"class": "unf-prop-list-prop"}).text.strip()
                if ('Apple' in islemci_model):
                    islemci_nesli.append(islemci_model)
                else:
                    islemci_nesli.append(find_gen(islemci_model))

            elif (('Model' in data.text) & ('İşlemci' not in data.text) & ('Ekran' not in data.text)):
                temp = data.find("p", {"class": "unf-prop-list-prop"}).text.strip()
                temp = temp.upper()
                model.append(temp)

            if (control == 0):
                if ('SSD' in isim[-1]):
                    disk_turu.append("SSD")
                elif ('HDD' in isim[-1]):
                    disk_turu.append("HDD")
    except:
        ind = listUniqueTrendyol.index(k)
        listUniqueTrendyol.pop(ind)
        listUniqueHepsiburada.pop(ind)
        listUniqueTeknosa.pop(ind)
        listUniqueN11.pop(ind)

no = insertDb("N11", no)

for k in listUniqueTrendyol:
    soup = get_soup(k)

    puanTrendyol.append("0.0")

    try:
        price = soup.find("div", {"class": "pr-bx-nm with-org-prc"}).text
        temp = price.split(" ")
        temp = temp[0]
        temp1 = temp.replace(".","")
        if (',' in temp1):
            fiyatTrendyol.append(temp1)
        else:
            temp2 = temp1 + ",00"
            fiyatTrendyol.append(temp2)
    except:
        ind = listUniqueTrendyol.index(k)
        listUniqueTrendyol.pop(ind)
        listUniqueHepsiburada.pop(ind)
        listUniqueTeknosa.pop(ind)
        listUniqueN11.pop(ind)


no = insertDb("TRENDYOL",no)

for k in listUniqueTeknosa:
    soup = get_soup(k)

    try:
        price = soup.find("span", attrs={'class': 'prc'}).text
        temp = price.split(" ")
        temp = temp[0]
        temp1 = temp.replace(".","")
        if(',' in temp1):
            fiyatTeknosa.append(temp1)
        else:
            temp2 = temp1 + ",00"
            fiyatTeknosa.append(temp2)

    except:
        ind = listUniqueTrendyol.index(k)
        listUniqueTrendyol.pop(ind)
        listUniqueHepsiburada.pop(ind)
        listUniqueTeknosa.pop(ind)
        listUniqueN11.pop(ind)
    puanTeknosa.append("0.0")

no = insertDb("TEKNOSA",no)

for k in listUniqueHepsiburada:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}
    r = requests.get(k, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    try:
        price = soup.find("span", attrs={"id": "offering-price"})
        temp = price["content"].strip()
        temp1 = temp.replace(".",",")
        fiyatHepsiburada.append(temp1)
    except:
        ind = listUniqueTrendyol.index(k)
        listUniqueTrendyol.pop(ind)
        listUniqueHepsiburada.pop(ind)
        listUniqueTeknosa.pop(ind)
        listUniqueN11.pop(ind)

    rating = soup.find("span", {"class": "rating-star"})
    if (rating == None):
        puanHepsiburada.append("0,0")
    else:
        temp = rating.text.strip()
        puanHepsiburada.append(temp)

no = insertDb("HEPSIBURADA",no)
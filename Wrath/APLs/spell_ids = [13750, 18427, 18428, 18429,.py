spell_ids = [13750, 18427, 18428, 18429, 13852, 84652, 84653, 84654, 79123, 79125, 13877, 31124, 31126, 31228, 31229, 31230, 14177, 35541, 35550, 35551, 14162, 14163, 14164, 51664, 51665, 51667, 31380, 31382, 31383, 30902, 30903, 30904, 30905, 30906, 51625, 51626, 79121, 79122, 13713, 13853, 13854, 14082, 14083, 13981, 14066, 79150, 79151, 79152, 31211, 31212, 31213, 58414, 58415, 51632, 91023, 13960, 13961, 13962, 30894, 30895, 16511, 51698, 51700, 51701, 14079, 14080, 84661, 14168, 14169, 13741, 13793, 13754, 13867, 14174, 14175, 14176, 14113, 14114, 14115, 14116, 14117, 79007, 79008, 13732, 13863, 79004, 14165, 14166, 13743, 13875, 13976, 13979, 51690, 14128, 14132, 14135, 13712, 13788, 13789, 14138, 14139, 14140, 14141, 14142, 31223, 58410, 14158, 14159, 1329, 31130, 31131, 13975, 14062, 14057, 14072, 79141, 58426, 13705, 13832, 13843, 14183, 14185, 51685, 51686, 51687, 51688, 51689, 13733, 13865, 13866, 31244, 31245, 31208, 31209, 79077, 79079, 14179, 58422, 58423, 14144, 14148, 79095, 79096, 84617, 14251, 14156, 14160, 14161, 79146, 79147, 51682, 58413, 14186, 14190, 14171, 14172, 13983, 14070, 14071, 51713, 36554, 31220, 51708, 51709, 51710, 32601, 5952, 51679, 51627, 51628, 51629, 51672, 51674, 79140, 79133, 79134, 14983, 16513, 16514, 16515, 61329, 51692, 51696, 30919, 30920
] 
output_file = r"data.lua"

import requests
from bs4 import BeautifulSoup
import json

def get_spell_data(spell_id):
    url = f"https://www.wowhead.com/cata/spell={spell_id}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        spell_data = {}
        
        # Extracting name
        title_tag = soup.find("title")
        if title_tag:
            name = title_tag.string.split(' - ')[0]
            name = re.sub(r'[\s_]+','_',name)
            name = re.sub(r'[^a-zA-Z_]+','',name)
            spell_data['name'] = name
        
        # Extracting description
        description_tag = soup.find("meta", {"name": "description"})
        if description_tag:
            description = description_tag.get('content', '')
            spell_data['description'] = description
        
        # Extracting cost
        cost_tag = soup.find("th", text="Cost")
        if cost_tag:
            cost = cost_tag.find_next("td").string.strip()
            spend = cost.split(' ')[0]
            spell_data['spend'] = (int(spend[:-1])/100 if "%" in spend else spend) if cost.strip()!="None" else ""
            try:
                spell_data['spendType'] = (cost.split(' ')[1:][-1]).lower()
            except:
                spell_data['spendType'] =''
        
        # Extracting cast time
        cast_tag = soup.find("th", text="Cast time")
        if cast_tag:
            cast = cast_tag.find_next("td").string.strip()
            spell_data['cast_time'] = cast.split(' ')[0]
        
        # Extracting cooldown
        cooldown_tag = soup.find("th", text="Cooldown")
        if cooldown_tag:
            cooldown = cooldown_tag.find_next("td").string.strip()
            spell_data['cooldown'] = cooldown
        
        # Extracting GCD
        gcd_tag = soup.find("th", text="GCD")
        if gcd_tag:
            gcd = gcd_tag.find_next("td").string.strip()
            spell_data['gcd'] = gcd.split(' ')[0]
        
        # Extracting forms
        forms_tag = soup.find("th", text="Forms")
        if forms_tag:
            forms = forms_tag.find_next("td").string.strip()
            spell_data['stance'] = forms

        # Extracting triggersId
        #triggers_tag = soup.find("a", href=re.compile(r"/cata/spell=\d+/.+"))
        #if triggers_tag:
        #    triggers_href = triggers_tag.get('href', '')
        for link in soup.select('a'):
            if link.get('href') != None:
                if '/cata/spell=' in link.get('href'):
                    #print(link.get('href'))
                    if link.get('href'):
                        spell_data['triggers_id'] = link.get('href')

        # Extracting image number
        image_tag = soup.find("link", rel="image_src")
        if image_tag:
            image_src = image_tag.get('href', '')
            image_number = re.search(r'/(\d+)\.jpg', image_src)
            if image_number:
                spell_data['texture'] = image_number.group(1)
        
        return spell_data
    else:
        print(f"Failed to fetch data for spell ID {spell_id}")
        return None
def map_gcd(gcd:str):
    if gcd == '0':
        return 'off'
    elif gcd == '1':
        return 'totem'
    else:
        return 'spell'

# Main:
spell_data_list = []
for spell_id in spell_ids:
    spell_data = get_spell_data(spell_id)
    if spell_data:
        #print(f"Spell ID: {spell_id}")
        #print(spell_data)
        #print("\n")
        spendstring = "" if not spell_data['spend'] else f'''spend = {spell_data['spend']}, \n        spendType = "{spell_data['spendType']}",'''
        spell_data_list.append(
            f'''    --{spell_data['description']}
    {spell_data['name'].lower()} = {{
        id = {spell_id},
        cast = {spell_data['cast_time'] if spell_data['cast_time'] != 'Instant' else 0},
        cooldown = {spell_data['cooldown'].split(' ')[0] if spell_data['cooldown']!='n/a' else 0},
        gcd = "{map_gcd(spell_data['gcd'])}",

        {spendstring}

        startsCombat = true,
        texture = {spell_data['texture']},

        --fix:
        stance = "{spell_data.get('stance')}",
        handler = function()
            --"{spell_data['triggers_id']}"
        end,

    }},''')
        
with open(output_file, 'w') as f:
    f.write("\n".join(spell_data_list))

print(f"Spell data written to {output_file}")

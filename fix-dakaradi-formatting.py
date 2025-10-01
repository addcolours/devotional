#!/usr/bin/env python3
"""
Fix formatting for dakaradi-sree-durga-sahasra-nama-stotram-english.php
"""

import re

def fix_dakaradi_formatting():
    file_path = "output_pages/en/dakaradi-sree-durga-sahasra-nama-stotram-english.php"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the content section
        start_marker = '                        <p>'
        end_marker = '</p></span>'
        
        start_index = content.find(start_marker)
        end_index = content.find(end_marker) + len(end_marker)
        
        if start_index != -1 and end_index != -1:
            # Extract the raw content
            raw_content = content[start_index + len(start_marker):end_index - len(end_marker)]
            
            # Clean up the content and format it properly
            lines = raw_content.split()
            formatted_content = []
            
            # Add the opening
            formatted_content.append('<p>śrī dēvyuvācha ।</p>')
            formatted_content.append('')
            formatted_content.append('<p>mama nāma sahasraṃ cha śiva pūrvavinirmitam ।<br>')
            formatted_content.append('tatpaṭhyatāṃ vidhānēna tathā sarvaṃ bhaviṣyati ॥</p>')
            formatted_content.append('')
            formatted_content.append('<p>ityuktvā pārvatī dēvi śrāvayāmāsa tachchatān ।<br>')
            formatted_content.append('tadēva nāmasāhasraṃ dakārādi varānanē ॥</p>')
            formatted_content.append('')
            formatted_content.append('<p>rōgadāridryadaurbhāgyaśōkaduḥkhavināśakam ।<br>')
            formatted_content.append('sarvāsāṃ pūjitaṃ nāma śrīdurgādēvatā matā ॥</p>')
            formatted_content.append('')
            formatted_content.append('<p>nijabījaṃ bhavēdbījaṃ mantraṃ kīlakamuchyatē ।<br>')
            formatted_content.append('sarvāśāpūraṇē dēvī viniyōgaḥ prakīrtitaḥ ॥</p>')
            formatted_content.append('')
            formatted_content.append('<p><strong>ōṃ asya śrīdakārādi durgāsahasranāma stōtrasya śiva ṛṣiḥ anuṣṭupChandaḥ śrīdurgā dēvatā duṃ bījaṃ duṃ kīlakaṃ duḥkhadāridryarōgaśōka nivṛttyarthaṃ pāṭhē viniyōgaḥ ।</strong></p>')
            formatted_content.append('')
            formatted_content.append('<p><strong>dhyānam</strong></p>')
            formatted_content.append('<p>vidyuddāmasamaprabhāṃ mṛgapati skandhasthitāṃ bhīṣaṇāṃ<br>')
            formatted_content.append('kanyābhiḥ karavālakhēṭaviladdastābhirāsēvitām ।<br>')
            formatted_content.append('hasaiśchakragadāsikhēṭa viśikhāṃśchāpaṃ guṇaṃ tarjanīṃ<br>')
            formatted_content.append('bibhrāṇāmanalātmikāṃ śaśidharāṃ durgāṃ trinētrāṃ bhajē ॥</p>')
            formatted_content.append('')
            formatted_content.append('<p><strong>stōtram</strong></p>')
            
            # Process the names (verses 1-226)
            current_verse = 1
            current_line = []
            
            # Split the content into words and process them
            words = raw_content.split()
            i = 0
            while i < len(words):
                word = words[i]
                
                # Check if this is a verse number
                if word == '॥' and i + 1 < len(words) and words[i + 1].isdigit():
                    # End current verse
                    if current_line:
                        formatted_content.append(f'<p>{" ".join(current_line)} ॥ {current_verse} ॥</p>')
                        current_line = []
                        current_verse += 1
                    i += 2
                elif word == '॥' and i + 1 < len(words) and words[i + 1] == '॥':
                    # End of all verses
                    if current_line:
                        formatted_content.append(f'<p>{" ".join(current_line)} ॥ {current_verse} ॥</p>')
                    break
                else:
                    current_line.append(word)
                    i += 1
            
            # Add the phalaśṛtiḥ section
            formatted_content.append('')
            formatted_content.append('<p><strong>phalaśṛtiḥ</strong></p>')
            formatted_content.append('<p>yaḥ paṭhētsādhakādhīśaḥ sarvasiddhirlabhēttu saḥ ।<br>')
            formatted_content.append('prātarmadhyāhnakālē cha sandhyāyāṃ niyataḥ śuchiḥ ॥227॥</p>')
            formatted_content.append('')
            formatted_content.append('<p>tathā\'rdharātrasamayē sa mahēśa ivāparaḥ ।<br>')
            formatted_content.append('śaktiyuktā mahārātrau mahāvīraḥ prapūjayēt ॥228॥</p>')
            formatted_content.append('')
            formatted_content.append('<p>mahādēvīṃ makārādyaiḥ pañchabhirdravya sattamaiḥ ।<br>')
            formatted_content.append('tatpaṭhēt stutimimāṃ yaḥ sa cha siddhisvarūpadhṛk ॥229॥</p>')
            formatted_content.append('')
            formatted_content.append('<p>dēvālayē śmaśānē cha gaṅgātīrē nijēgṛhē ।<br>')
            formatted_content.append('vārāṅganāgṛhē chaiva śrīgurōḥ sannidhānapi ॥230॥</p>')
            formatted_content.append('')
            formatted_content.append('<p>parvatē prāntarē ghōrē stōtramētatsadā paṭhēt ।<br>')
            formatted_content.append('durgānāmasahasrēṇa durgāṃ paśyati chakṣuṣā ॥231॥</p>')
            formatted_content.append('')
            formatted_content.append('<p>śatāvartanamētasya puraścharaṇamuchyatē ।<br>')
            formatted_content.append('stutisārō nigaditaḥ kiṃ bhūyaḥ śrōtumichChasi ॥232॥</p>')
            formatted_content.append('')
            formatted_content.append('<p>iti kulārṇavē durgā dakārādi sahasranāmastōtram ।</p>')
            
            # Join all formatted content
            new_content = '\n                        '.join(formatted_content)
            
            # Replace the content
            updated_content = content[:start_index] + new_content + content[end_index:]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"✅ Successfully formatted {file_path}")
            return True
            
    except Exception as e:
        print(f"❌ Error formatting {file_path}: {e}")
        return False

if __name__ == "__main__":
    fix_dakaradi_formatting()

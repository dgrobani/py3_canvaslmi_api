from canvas.core.courses import create_course, create_enrollment, copy_course
from canvas.core.io import tada

from canvas.core.users import get_user_by_sis_id

r_and_p_account_id = '146275'
r_and_p_template_course_id = '1963445'
sis_user_ids = ['P000040481', 'P000055601', 'P000068861', 'P000040372', 'P000069505', 'P000040283', 'P000040412',
                'P000003248', 'P000075574', 'P000056769', 'P000064217', 'P000049558', 'P000064103', 'P000069775',
                'P000006331', 'P000040574', 'P000106163', 'P000059358', 'P000040606', 'P000043808', 'P000108803',
                'P000000212', 'P000105812', 'P000086630', 'P000064215', 'P000070340', 'P000069860', 'P000105448',
                'P000054690', 'P000004541', 'P000040378', 'P000009891', 'P000106070', 'P000040504', 'P000040613',
                'P000056504', 'P000040298', 'P000063249', 'P000056603', 'P000097470', 'P000040736', 'P000040402',
                'P000040386', 'P000039252', 'P000039519', 'P000040633', 'P000105863', 'P000000205', 'P000023419',
                'P000056600', 'P000040302', 'P000085673', 'P000059725', 'P000049423', 'P000050098', 'P000103897',
                'P000002939', 'P000067085', 'P000040311', 'P000069288', 'P000069771', 'P000100575', 'P000040737',
                'P000068849', 'P000098871', 'P000072676', 'P000001403', 'P000068101', 'P000082406', 'P000108497',
                'P000041263', 'P000111981', 'P000075546', 'P000082208', 'P000059748', 'P000040539', 'P000039450',
                'P000040430', 'P000098449', 'P000092634', 'P000083197', 'P000058289', 'P000000117', 'P000066320',
                'P000082623', 'P000040636', 'P000062385', 'P000065050', 'P000063248', 'P000095767', 'P000088167',
                'P000040557', 'P000047590', 'P000040531', 'P000040748', 'P000099972', 'P000074485', 'P000068631',
                'P000058155', 'P000004225', 'P000088203', 'P000093330', 'P000056766', 'P000064484', 'P000082347',
                'P000040573', 'P000076569', 'P000040532', 'P000000080', 'P000061604', 'P000107470', 'P000043871',
                'P000070466', 'P000074484', 'P000062126', 'P000034023', 'P000088215', 'P000059786', 'P000040724',
                'P000066056', 'P000110227', 'P000052981', 'P000082712', 'P000069214']
for sis_user_id in sis_user_ids:
    course_code = 'R&P ePortfolio: ' + get_user_by_sis_id(sis_user_id)['name']
    print(course_code)
    #### changed create_course() to return course instead of course_id 2017.02.22, added "['id']", needs testing
    new_course_id = create_course(r_and_p_account_id, course_code, course_code)['id']
    create_enrollment(new_course_id, 'sis', sis_user_id, 'teacher')
    copy_course(r_and_p_template_course_id, new_course_id)
tada()

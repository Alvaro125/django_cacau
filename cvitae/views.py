import io
import requests
from datetime import datetime

from pyexpat.errors import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from django.conf import settings
from django.http import HttpResponse

from accounts.serializers import CustomUserSerializer
from cvitae.models import CVitae
from cvitae.serializers import CVitaeSerializer
from profiles.models import Project, Profile, Skill, Course, Language, Experience, Degree, Certificate
from profiles.serializers import ProfileSerializer, SkillSerializer, LanguageSerializer, ExperienceSerializer, \
    CourseSerializer, DegreeSerializer, CertificateSerializer, ProjectSerializer
from openai import OpenAI

class CVitaeViewSet(viewsets.ModelViewSet):
    queryset = CVitae.objects.all()
    serializer_class = CVitaeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CVitae.objects.filter(user=self.request.user)
class MarkdownCreateView(APIView):
    def post(self, request):
        client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        profile = Profile.objects.get(user=request.user)

        # Serialize all the related data
        user = CustomUserSerializer(request.user).data
        profile_data = ProfileSerializer(profile).data
        skills_data = SkillSerializer(Skill.objects.filter(profile=profile), many=True).data
        languages_data = LanguageSerializer(Language.objects.filter(profile=profile), many=True).data
        experiences_data = ExperienceSerializer(Experience.objects.filter(profile=profile), many=True).data
        courses_data = CourseSerializer(Course.objects.filter(profile=profile), many=True).data
        degrees_data = DegreeSerializer(Degree.objects.filter(profile=profile), many=True).data
        certificates_data = CertificateSerializer(Certificate.objects.filter(profile=profile), many=True).data
        projects_data = ProjectSerializer(Project.objects.filter(profile=profile), many=True).data

        # Combine all data into a single response
        cv = {
            "user": user,
            'profile': profile_data,
            'skills': skills_data,
            'languages': languages_data,
            'experiences': experiences_data,
            'courses': courses_data,
            'degrees': degrees_data,
            'certificates': certificates_data,
            'projects': projects_data
        }
        msg = request.data.get("msg")

        if not msg:
            return Response({"error": "Campo 'msg' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[
                {"role": "system", "content": """
📄 Content System: Geração de Currículos de Alto Impacto para ATS

🧩 Estrutura Padrão do Currículo:

1. Cabeçalho
- Nome completo
- Cargo-alvo (ex: Desenvolvedor Front-end React | TypeScript | Redux)
- E-mail profissional
- LinkedIn | GitHub | Portfólio

2. Resumo Profissional (3–5 linhas)
- Quem é você profissionalmente
- Quantos anos de experiência
- Áreas de especialização e tecnologias-chave
- Principais conquistas

Exemplo:
Desenvolvedor Front-end com 3+ anos de experiência em React, TypeScript e Redux. Especialista em criar interfaces performáticas, responsivas e acessíveis. Reduzi em 40% o tempo de carregamento de aplicações em produção. Experiência em times ágeis e foco em entregas com impacto.

3. Experiência Profissional (ordem cronológica inversa)
- Título do cargo | Nome da empresa | Cidade, Estado | [Mês/Ano] – [Mês/Ano]
- Stack: React, TypeScript, Styled Components
- Principais entregas (bullet points com impacto):
  - Criei interface responsiva com React, reduzindo tempo de carregamento em 40%
  - Implementei sistema de autenticação com JWT, aumentando segurança da plataforma
  - Liderei migração de CSS para Styled Components em 3 projetos

4. Formação Acadêmica
- Nome do curso | Instituição | Conclusão [Ano]
- (Adicione projetos relevantes, se aplicável)

5. Certificações
- Nome do certificado | Instituição | Data de emissão

6. Habilidades Técnicas
- Linguagens: JavaScript, TypeScript, Python
- Frameworks: React, Next.js, Django
- Ferramentas: Git, Figma, Docker
- Soft Skills: Comunicação, Resolução de problemas, Trabalho em equipe

7. Idiomas
- Inglês – Avançado
- Espanhol – Intermediário

8. Projetos Pessoais (se relevantes)
- Título | Stack usada | Link
- Breve descrição e impacto (ex: API RESTful com Django, usada por 200+ usuários)

🛑 Erros a Evitar:
❌ "Criação de página com React." → ✅ "Criei página com React, reduzindo tempo de carregamento em 40%."
❌ "Freelancer" → ✅ "Desenvolvedor Front-end React | TypeScript | Redux"
❌ Tabelas e colunas → ✅ Layout simples e linear
❌ Arquivo com imagem ou texto não selecionável → ✅ PDF com texto selecionável
❌ Fontes não padrão → ✅ Arial, Calibri ou Times New Roman
❌ Títulos genéricos → ✅ Use: Experiência Profissional, Formação, Habilidades, Projetos

🔁 Checklist Final (antes de enviar):
- [ ] Sem tabelas ou gráficos
- [ ] Palavras-chave da vaga incluídas no texto
- [ ] Stack visível nas experiências
- [ ] Resultados com números (aumento, redução, impacto)
- [ ] Revisado ortograficamente
- [ ] Link do LinkedIn atualizado
Obs: a resposta deve ser somente o curriculo, sem observações, dicas ou introduções desnecessarias
"""},
                {
                    "role": "user",
                    "content": str(cv)
                },
                {
                    "role": "user",
                    "content": f"vaga que deseja aplicar: {msg}"
                }
            ]
        )

        # Get the content from the OpenAI response
        cv_content = response.choices[0].message.content

        try:
            # Prepare the markdown content in memory
            markdown_content = cv_content
            file_buffer = io.BytesIO(markdown_content.encode("utf-8"))

            # Prepare filename for the markdown file
            filename = f"cv_{request.user.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

            # Option 1: Save to local storage if needed
            # with open(f"{settings.MEDIA_ROOT}/cvs/{filename}", "wb") as f:
            #     f.write(file_buffer.getvalue())

            # Option 2: Return the markdown directly as response
            # return HttpResponse(
            #     file_buffer.getvalue(),
            #     content_type='text/markdown; charset=utf-8',
            #     headers={'Content-Disposition': f'attachment; filename="{filename}"'}
            # )

            # Option 3: Upload to Pinata
            files = {
                "file": (filename, file_buffer, "text/plain")
            }

            data = {
                "network": "public"
            }

            # Add group if defined
            if hasattr(settings, 'PINATA_GROUP') and settings.PINATA_GROUP:
                data["group"] = settings.PINATA_GROUP

            # Make request to Pinata v3
            headers = {
                "Authorization": f"Bearer {settings.PINATA_API_JWT}",
            }

            pinata_response = requests.post(
                "https://uploads.pinata.cloud/v3/files",
                headers=headers,
                files=files,
                data=data
            )

            if pinata_response.status_code == 200:
                json_data = pinata_response.json()
                CVitae.objects.create(user=request.user,
                                      url=f"https://orange-quarrelsome-mosquito-548.mypinata.cloud/ipfs/{json_data['data']['cid']}",
                                      content=msg)
                return Response({
                    "resposta": cv_content,  # Return the raw CV content as well
                    "markdown_url": f"https://orange-quarrelsome-mosquito-548.mypinata.cloud/ipfs/{json_data['data']['cid']}",
                    "cid": json_data['data']["cid"],
                    "size": json_data['data']["size"],
                    "created_at": json_data['data']["created_at"]
                }, status=status.HTTP_201_CREATED)
            else:
                # If Pinata fails, still return the CV content
                return Response({
                    "resposta": cv_content,
                    "erro_markdown": pinata_response.text
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Return the CV content even if markdown handling fails
            return Response({
                "resposta": cv_content,
                "erro_markdown": str(e)
            }, status=status.HTTP_201_CREATED)
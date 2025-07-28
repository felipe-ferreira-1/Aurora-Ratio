import requests # pyright: ignore[reportMissingModuleSource]

# 🔗 Supabase URL e chave pública
url = "https://wegwcsfapippzwiltmtg.supabase.co"  # substitua pela sua URL real
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndlZ3djc2ZhcGlwcHp3aWx0bXRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI1MTE1MDksImV4cCI6MjA2ODA4NzUwOX0._pNWbPt_6Wpmm89mPrZ2aXPTxsPvrLk1taTpXkVdmpY"  # substitua pela sua chave real

headers = {
    "Content-Type": "application/json",
    "apikey": key,
    "Authorization": f"Bearer {key}"
}

# 🧩 Nome atualizado da tabela
table = "posts_comunidade"

# ✅ Criar post
def create_post(title, content, author=""):
    data = {
        "title": title,
        "content": content,
        "author": author
    }
    response = requests.post(f"{url}/rest/v1/{table}", headers=headers, json=data)
    if response.status_code == 201:
        print("✅ Post criado com sucesso!")
    else:
        print("⚠️ Erro ao criar post:", response.text)

# 📋 Listar todos os posts
def list_posts():
    response = requests.get(f"{url}/rest/v1/{table}?select=*", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("⚠️ Erro ao listar posts:", response.text)
        return []

# 🗑️ Deletar post por ID
def delete_post(post_id):
    response = requests.delete(f"{url}/rest/v1/{table}?id=eq.{post_id}", headers=headers)
    if response.status_code == 204:
        print(f"🗑️ Post {post_id} deletado com sucesso!")
    else:
        print("⚠️ Erro ao deletar post:", response.text)

# ✏️ Atualizar post por ID
def update_post(post_id, title=None, content=None, author=None):
    update_data = {}
    if title: update_data["title"] = title
    if content: update_data["content"] = content
    if author is not None: update_data["author"] = author

    response = requests.patch(f"{url}/rest/v1/{table}?id=eq.{post_id}", headers=headers, json=update_data)
    if response.status_code == 204:
        print(f"🔄 Post {post_id} atualizado com sucesso!")
    else:
        print("⚠️ Erro ao atualizar post:", response.text)
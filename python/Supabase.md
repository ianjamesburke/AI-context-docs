# supabase python examples

### Initialize supabase client
import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Insert data
response = (
    supabase.table("countries")
    .insert({"id": 1, "name": "Denmark"})
    .execute()
)

# Update data
response = (
    supabase.table("countries")
    .update({"name": "Australia"})
    .eq("id", 1)
    .execute()
)


# sign in user
response = supabase.auth.sign_in_with_password(
    {"email": "email@example.com", "password": "example-password"}
)

response = supabase.auth.sign_out()



# new user 
response = supabase.auth.sign_up(
    {"email": "email@example.com", "password": "password"}
)

supabase.auth.reset_password_for_email(email, {
  "redirect_to": "https://example.com/update-password",
})



# Storage
response = supabase.storage.create_bucket('avatars',   
  options={
    "public": False,
    "allowed_mime_types": ["image/png"],
    "file_size_limit": 1024,
  }
)

response = supabase.storage.get_bucket('avatars')

response = supabase.storage.list_buckets()
response = supabase.storage.update_bucket('avatars',   
  options={
    "public": False,
    "allowed_mime_types": ["image/png"],
    "file_size_limit": 1024,
  }
)
response = supabase.storage.delete_bucket('avatars')
response = supabase.storage.empty_bucket('avatars')
with open('./public/avatar1.png', 'rb') as f:
  response = supabase.storage.from_("avatars").upload(
      file=f,
      path="public/avatar1.png",
      file_options={"cache-control": "3600", "upsert": "false"},
  )
with open("./myfolder/avatar1.png", "wb+") as f:
  response = supabase.storage.from_("avatars").download(
    "folder/avatar1.png"
  )
  f.write(response)
response = supabase.storage.from_("avatars").list(
  "folder",
  {"limit": 100, "offset": 0, "sortBy": {"column": "name", "order": "desc"}},
)
response = supabase.storage.from_("avatars").move(
  "public/avatar1.png", "private/avatar2.png"
)
response = supabase.storage.from_("avatars").copy(
  "public/avatar1.png", "private/avatar2.png"
)
response = supabase.storage.from_('avatars').remove(['folder/avatar1.png'])
response = supabase.storage.from_("avatars").create_signed_url(
  "folder/avatar1.png", 60
)
response = supabase.storage.from_("avatars").create_signed_urls(
  ["folder/avatar1.png", "folder/avatar2.png"], 60
)
response = supabase.storage.from_("avatars").create_signed_upload_url(
  "folder/avatar1.png"
)
with open("./public/avatar1.png", "rb") as f:
  response = supabase.storage.from_("avatars").upload_to_signed_url(
      path="folder/cat.jpg",
      token="token-from-create_signed_upload_url",
      file=f,
  )
response = supabase.storage.from_("avatars").get_public_url(
  "folder/avatar1.jpg"
)


# third party sign in
response = supabase.auth.sign_in_with_oauth({
  "provider": 'github'
})
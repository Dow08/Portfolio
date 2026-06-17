# Bucket S3 principal - stockage des images produits PixelStore
resource "aws_s3_bucket" "media" {
  bucket = "${var.project_name}-${var.env}-media"

  tags = {
    Name        = "${var.project_name}-${var.env}-media"
    Environment = var.env
    Owner       = var.owner
  }
}

# Versioning - protection contre la suppression accidentelle
resource "aws_s3_bucket_versioning" "media" {
  bucket = aws_s3_bucket.media.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Chiffrement au repos - toutes les images sont chiffrées automatiquement
resource "aws_s3_bucket_server_side_encryption_configuration" "media" {
  bucket = aws_s3_bucket.media.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Blocage accès public - aucun accès direct depuis internet
resource "aws_s3_bucket_public_access_block" "media" {
  bucket = aws_s3_bucket.media.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# ---------------------------------------------------------------------------
# Upload app.zip - le code Flask complet
# ---------------------------------------------------------------------------
resource "aws_s3_object" "app_zip" {
  bucket = aws_s3_bucket.media.id
  key    = "app/app.zip"
  source = "${path.root}/app.zip"
  etag   = filemd5("${path.root}/app.zip")

  tags = {
    Name        = "app-zip"
    Environment = var.env
    Owner       = var.owner
  }
}

# ---------------------------------------------------------------------------
# Upload images produits
# ---------------------------------------------------------------------------
resource "aws_s3_object" "image_iphone16promax" {
  bucket       = aws_s3_bucket.media.id
  key          = "images/iphone16promax.jpg"
  source       = "${path.root}/app/static/img/iphone16promax.jpg"
  etag         = filemd5("${path.root}/app/static/img/iphone16promax.jpg")
  content_type = "image/jpeg"
}

resource "aws_s3_object" "image_iphone16pro" {
  bucket       = aws_s3_bucket.media.id
  key          = "images/iphone16pro.jpg"
  source       = "${path.root}/app/static/img/iphone16pro.jpg"
  etag         = filemd5("${path.root}/app/static/img/iphone16pro.jpg")
  content_type = "image/jpeg"
}

resource "aws_s3_object" "image_iphone16" {
  bucket       = aws_s3_bucket.media.id
  key          = "images/iphone16.jpg"
  source       = "${path.root}/app/static/img/iphone16.jpg"
  etag         = filemd5("${path.root}/app/static/img/iphone16.jpg")
  content_type = "image/jpeg"
}

resource "aws_s3_object" "image_s25ultra" {
  bucket       = aws_s3_bucket.media.id
  key          = "images/s25ultra.jpg"
  source       = "${path.root}/app/static/img/s25ultra.jpg"
  etag         = filemd5("${path.root}/app/static/img/s25ultra.jpg")
  content_type = "image/jpeg"
}

resource "aws_s3_object" "image_s25plus" {
  bucket       = aws_s3_bucket.media.id
  key          = "images/s25plus.jpg"
  source       = "${path.root}/app/static/img/s25plus.jpg"
  etag         = filemd5("${path.root}/app/static/img/s25plus.jpg")
  content_type = "image/jpeg"
}

resource "aws_s3_object" "image_zfold6" {
  bucket       = aws_s3_bucket.media.id
  key          = "images/zfold6.jpg"
  source       = "${path.root}/app/static/img/zfold6.jpg"
  etag         = filemd5("${path.root}/app/static/img/zfold6.jpg")
  content_type = "image/jpeg"
}

resource "aws_s3_object" "image_pixel9proxl" {
  bucket       = aws_s3_bucket.media.id
  key          = "images/pixel9proxl.jpg"
  source       = "${path.root}/app/static/img/pixel9proxl.jpg"
  etag         = filemd5("${path.root}/app/static/img/pixel9proxl.jpg")
  content_type = "image/jpeg"
}

resource "aws_s3_object" "image_pixel9pro" {
  bucket       = aws_s3_bucket.media.id
  key          = "images/pixel9pro.jpg"
  source       = "${path.root}/app/static/img/pixel9pro.jpg"
  etag         = filemd5("${path.root}/app/static/img/pixel9pro.jpg")
  content_type = "image/jpeg"
}

resource "aws_s3_object" "image_pixel9" {
  bucket       = aws_s3_bucket.media.id
  key          = "images/pixel9.jpg"
  source       = "${path.root}/app/static/img/pixel9.jpg"
  etag         = filemd5("${path.root}/app/static/img/pixel9.jpg")
  content_type = "image/jpeg"
}

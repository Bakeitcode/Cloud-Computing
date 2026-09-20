terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"     #TODO: Set the region
}

# ─────────────────────────────────────────
# S3 BUCKET
# ─────────────────────────────────────────

resource "aws_s3_bucket" "website" {
  bucket        = "class-terraform-bucket-acr22003"   # TODO:  name the bucket
  force_destroy = true
}

# TODO: set the 4 required values below, either true or false
resource "aws_s3_bucket_public_access_block" "website" {
  bucket                  = aws_s3_bucket.website.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_website_configuration" "website" {
  bucket = aws_s3_bucket.website.id

  index_document {
    suffix = "index.html"
  }
}

resource "aws_s3_bucket_policy" "public_read" {
  bucket     = aws_s3_bucket.website.id
  depends_on = [aws_s3_bucket_public_access_block.website]

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid       = "PublicReadGetObject"
      Effect    = "Allow"
      Principal = "*"
      Action    = "s3:GetObject"
      Resource  = "${aws_s3_bucket.website.arn}/*"
    }]
  })
}

# ─────────────────────────────────────────
# INDEX.HTML (inline — no separate file needed)
# ─────────────────────────────────────────

# TODO: add additional html code between the <html> and </html> tags below
# Put the phrase "final four" in your html response

resource "aws_s3_object" "index" {
  bucket       = aws_s3_bucket.website.id
  key          = "index.html"
  content_type = "text/html"

  content = <<-HTML
    <!DOCTYPE html>
    <html>
    "We're in the final four!"
    </html>
  HTML
}

# ─────────────────────────────────────────
# OUTPUT
# ─────────────────────────────────────────

output "website_url" {
  value = "http://${aws_s3_bucket_website_configuration.website.website_endpoint}"
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }

  backend "s3" {
    bucket         = "projet-02-terraform-state"
    key            = "projet-02/terraform.tfstate"
    region         = "eu-west-3"
    dynamodb_table = "projet-02-terraform-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region
}

# Module VPC
module "vpc" {
  source       = "./modules/vpc"
  vpc_cidr     = var.vpc_cidr
  project_name = var.project_name
  env          = var.env
  owner        = var.owner
}

# Module Subnets
module "subnets" {
  source               = "./modules/subnets"
  vpc_id               = module.vpc.vpc_id
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  availability_zones   = var.availability_zones
  project_name         = var.project_name
  env                  = var.env
  owner                = var.owner
}

# Module IGW
module "igw" {
  source       = "./modules/igw"
  vpc_id       = module.vpc.vpc_id
  project_name = var.project_name
  env          = var.env
  owner        = var.owner
}

# Module NAT
module "nat" {
  source           = "./modules/nat"
  public_subnet_id = module.subnets.public_subnet_ids[0]
  project_name     = var.project_name
  env              = var.env
  owner            = var.owner
}

# Module Route Tables
module "route_tables" {
  source             = "./modules/route_tables"
  vpc_id             = module.vpc.vpc_id
  igw_id             = module.igw.igw_id
  nat_gateway_id     = module.nat.nat_gateway_id
  public_subnet_ids  = module.subnets.public_subnet_ids
  private_subnet_ids = module.subnets.private_subnet_ids
  project_name       = var.project_name
  env                = var.env
  owner              = var.owner
}

# Module Security Groups
module "security_groups" {
  source       = "./modules/security_groups"
  vpc_id       = module.vpc.vpc_id
  project_name = var.project_name
  env          = var.env
  owner        = var.owner
}

# Module NACL
module "nacl" {
  source             = "./modules/nacl"
  vpc_id             = module.vpc.vpc_id
  public_subnet_ids  = module.subnets.public_subnet_ids
  private_subnet_ids = module.subnets.private_subnet_ids
  project_name       = var.project_name
  env                = var.env
  owner              = var.owner
}

# Module Secrets Manager
module "secrets_manager" {
  source       = "./modules/secrets_manager"
  project_name = var.project_name
  env          = var.env
  owner        = var.owner
  db_username  = var.db_username
  db_password  = var.db_password
  db_name      = var.db_name
}

# Module IAM
module "iam" {
  source        = "./modules/iam"
  project_name  = var.project_name
  env           = var.env
  owner         = var.owner
  secret_arn    = module.secrets_manager.secret_arn
  s3_bucket_arn = module.s3.bucket_arn
}

# Module RDS
module "rds" {
  source                  = "./modules/rds"
  project_name            = var.project_name
  env                     = var.env
  owner                   = var.owner
  private_subnet_ids      = module.subnets.private_subnet_ids
  sg_rds_id               = module.security_groups.sg_rds_id
  db_username             = module.secrets_manager.db_username
  db_password             = var.db_password
  db_name                 = module.secrets_manager.db_name
  multi_az                = var.multi_az
  backup_retention_period = var.backup_retention_period
}

# Module ALB
module "alb" {
  source            = "./modules/alb"
  vpc_id            = module.vpc.vpc_id
  project_name      = var.project_name
  env               = var.env
  owner             = var.owner
  public_subnet_ids = module.subnets.public_subnet_ids
  sg_alb_id         = module.security_groups.sg_alb_id
}

# Module EC2 ASG
module "ec2_asg" {
  source                = "./modules/ec2_asg"
  project_name          = var.project_name
  env                   = var.env
  owner                 = var.owner
  public_subnet_ids     = module.subnets.public_subnet_ids
  sg_ec2_id             = module.security_groups.sg_ec2_id
  target_group_arn      = module.alb.target_group_arn
  db_host               = module.rds.db_host
  db_name               = module.rds.db_name
  db_username           = module.secrets_manager.db_username
  db_password           = var.db_password
  instance_type         = var.instance_type
  ami_id                = var.ami_id
  secret_arn            = module.secrets_manager.secret_arn
  instance_profile_name = module.iam.instance_profile_name
  s3_bucket_name        = module.s3.bucket_name
}

# Module WAF
module "waf" {
  source       = "./modules/waf"
  project_name = var.project_name
  env          = var.env
  owner        = var.owner
  alb_arn      = module.alb.alb_arn
}

# Module S3
module "s3" {
  source       = "./modules/s3"
  project_name = var.project_name
  env          = var.env
  owner        = var.owner
}

# Module CloudWatch
module "cloudwatch" {
  source                  = "./modules/cloudwatch"
  project_name            = var.project_name
  env                     = var.env
  owner                   = var.owner
  asg_name                = module.ec2_asg.asg_name
  alb_arn_suffix          = module.alb.alb_arn_suffix
  target_group_arn_suffix = module.alb.target_group_arn_suffix
  db_instance_identifier  = module.rds.db_instance_id
  alarm_email             = var.alarm_email
}

# Module CloudTrail
module "cloudtrail" {
  source       = "./modules/cloudtrail"
  project_name = var.project_name
  env          = var.env
  owner        = var.owner
}

# Module GuardDuty
module "guardduty" {
  source        = "./modules/guardduty"
  project_name  = var.project_name
  env           = var.env
  owner         = var.owner
  sns_topic_arn = module.cloudwatch.sns_topic_arn
}
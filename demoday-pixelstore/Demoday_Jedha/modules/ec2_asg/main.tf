# Launch Template
resource "aws_launch_template" "main" {
  name_prefix   = "${var.project_name}-lt-"
  image_id      = var.ami_id
  instance_type = var.instance_type

  iam_instance_profile {
    name = var.instance_profile_name
  }

  network_interfaces {
    associate_public_ip_address = true
    security_groups             = [var.sg_ec2_id]
  }

  user_data = base64encode(<<-EOF
#!/bin/bash
exec > /var/log/user-data.log 2>&1

echo "=== START USER DATA ==="

dnf update -y
dnf install -y python3 python3-pip unzip
echo "=== PACKAGES INSTALLED ==="

# Utilisateur de service non privilégié (moindre privilège)
id appuser &>/dev/null || useradd --system --no-create-home --shell /usr/sbin/nologin appuser

mkdir -p /app
aws s3 cp s3://${var.s3_bucket_name}/app/app.zip /app/app.zip --region eu-west-3
cd /app
unzip -o app.zip
rm -f app.zip
echo "=== APP UNZIPPED ==="

pip3 install -r /app/requirements.txt
echo "=== PIP DONE ==="

# L'app tourne en lecture seule sur son code
chown -R appuser:appuser /app
echo "=== PERMISSIONS SET ==="

cat > /etc/systemd/system/flask.service << SERVICEEOF
[Unit]
Description=PixelStore Flask App
After=network.target

[Service]
Type=simple
User=appuser
WorkingDirectory=/app
Environment="SECRET_ARN=${var.secret_arn}"
Environment="DB_HOST=${var.db_host}"
Environment="DB_NAME=${var.db_name}"
Environment="S3_BUCKET=${var.s3_bucket_name}"
Environment="AWS_REGION=eu-west-3"
# Serveur WSGI de production (F2) : plus de serveur de dev Werkzeug.
ExecStart=/usr/bin/python3 -m gunicorn --workers 3 --bind 0.0.0.0:5000 app:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICEEOF

systemctl daemon-reload
systemctl enable flask
systemctl start flask

echo "=== USER DATA COMPLETE ==="
EOF
  )

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name        = "${var.project_name}-ec2"
      Environment = var.env
      Owner       = var.owner
      ManagedBy   = "Terraform"
    }
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "main" {
  name                = "${var.project_name}-asg"
  vpc_zone_identifier = var.public_subnet_ids
  target_group_arns   = [var.target_group_arn]
  health_check_type   = "ELB"

  min_size         = var.min_size
  max_size         = var.max_size
  desired_capacity = var.desired_capacity

  launch_template {
    id      = aws_launch_template.main.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "${var.project_name}-asg-instance"
    propagate_at_launch = true
  }

  tag {
    key                 = "Environment"
    value               = var.env
    propagate_at_launch = true
  }

  tag {
    key                 = "Owner"
    value               = var.owner
    propagate_at_launch = true
  }
}

# Scaling Policy - scale up si CPU dépasse 60%
resource "aws_autoscaling_policy" "cpu_scale_up" {
  name                   = "${var.project_name}-cpu-scale-up"
  autoscaling_group_name = aws_autoscaling_group.main.name
  policy_type            = "TargetTrackingScaling"

  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }
    target_value = 60.0
  }
}
